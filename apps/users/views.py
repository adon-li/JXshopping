

from django.shortcuts import render

# Create your views here.
"""
检查用户名重复
前端：
 if (this.error_name == false) {
                var url = this.host + '/usernames/' + this.username + '/count/';
                axios.get(url, {
                    responseType: 'json',
                    withCredentials:true,
                })
后端：
接受请求，获取usernames，前端已经写明以get形式的发起请求链接
 var url = this.host + '/usernames/' + this.username + '/count/';
判断usernames是否重复
以json数据格式返回数据给前端  
 .then(response => {
                        if (response.data.count > 0) {
                            this.error_name_message = '用户名已存在';
                            this.error_name = true;
                        } else {
                            this.error_name = false;
                        }
                    })              
"""
from django.views import View
from apps.users.models import User
from django_redis import get_redis_connection
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from utils.encryption import generic_email_verify_token,check_verifu_token
from celery_work.email.tasks import celery_send_mail
import json
import re
class UsernameCount(View):
    def get(self,request,username):
        count = User.objects.filter(username=username).count()
        if count != 0:
            return JsonResponse({'code':'0','count':count,'errmsg':'ERROR'})
        return JsonResponse({'code': '0', 'count': count, 'errmsg': 'SUCCESS'})
class MobileCount(View):
    def get(self,request,mobile):
        count = User.objects.filter(mobile=mobile).count()
        if count != 0:
            return JsonResponse({'code':'0','count':count,'errmsg':'ERROR'})
        return JsonResponse({'code': '0', 'count': count, 'errmsg': 'SUCCESS'})

"""
前端：携带用户注册的信息，发送axios请求
    if (this.error_name == false && this.error_password == false && this.error_check_password == false
        && this.error_phone == false && this.error_sms_code == false && this.error_allow == false) {
        axios.post(this.host + '/register/', {
            username: this.username,
            password: this.password,
            password2: this.password2,
            mobile: this.mobile,
            sms_code: this.sms_code,
            allow: this.allow
        }, {
            responseType: 'json',
            withCredentials:true,
        })
后端：
接受数据
验证数据,数据入库
返回响应,JSON{"code":0,"errmsg":"ok"}
"""

class Register(View):
    def post(self,request):
        body_bytes = request.body
        # print(body_bytes)
        body_str = body_bytes.decode()
        body_dict = json.loads(body_str)
        # print(body_dict)
        username = body_dict.get('username')
        password = body_dict.get('password')
        password2 = body_dict.get('password2')
        mobile = body_dict.get('mobile')
        sms_code = body_dict.get('sms_code')
        allow = body_dict.get('allow')
        #all中的元素，只要是none，false，all就返回False，否则返回True
        if not all([username,password,password2,mobile,allow]):
            return JsonResponse({'code':400,'errmsg':'参数不全'})
        if not re.match('[a-zA-Z0-9_-]{5,20}',username):
            return JsonResponse({'code':400,'errmsg':'用户名不满足规则'})
        if not re.match('[a-zA-Z0-9_-]{8,20}',password):
            return JsonResponse({'code':400,'errmsg':'密码不满足规则'})
        if password !=password2:
            return JsonResponse({'code':400,'errmsg':'密码不一致'})
        if not re.match('^1[345789]\d{9}',mobile):
            return JsonResponse({'code':400,'errmsg':'手机号不满足规则'})
        if allow != True:
            return JsonResponse({'code':400,'errmsg':'allow格式有误'})

        redis_conn = get_redis_connection('code')
        redis_sms_code = redis_conn.get(mobile)
        if sms_code != redis_sms_code.decode():
            return JsonResponse({'code':400,'errmsg':'短信验证码错误'})

        try:
            user = User.objects.create_user(username=username,password=password,mobile=mobile)

        except Exception as e:
            return JsonResponse({'code':400,'errmsg':'注册失败！'})
        return JsonResponse({'code':400,'errmsg':'注册成功！'})

class Login(View):
    def post(self,request):
        data = json.loads(request.body.decode())
        username = data.get('username')
        password = data.get('password')
        remembered = data.get('remembered')
        #验证登录数据
        if not all([username,password]):
            return JsonResponse({'code':400,'errmsg':'参数不全'})
        #用户名为手机号时也可以登录。User.USERNAME_FIELD默认是数据库username查询。
        if re.match('1[3-9]\d{9}',username):
            User.USERNAME_FIELD='mobile'
        else:
            User.USERNAME_FIELD='username'
        #authenticate传递用户名和密码，如果有用户名和密码正确，返回User。否则返回None。
        user = authenticate(username=username,password=password)
        if user is None:
            return JsonResponse({'code':400,'errmsg':'参数错误'})
        #如果用户名密码正确，状态保持(session)
        login(request,user)

        if remembered:
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)
        response =  JsonResponse({'code':0,'errmsg':'OK'})
        response.set_cookie('username',username)
        return response

class Logout(View):
    def delete(self,request):
        #删除session信息，logout()中的request.session.flush()
        logout(request)
        #删除cookie信息，因为前端获取的cookie中的username
        response = JsonResponse({'code':0,'errmsg':'OK'})
        response.delete_cookie('username')
        return response

"""
LoginRequiredMixin,登录用户认证，未登录用户，返回重定向，但是前端需要的是json数据，
后端与前端通过json交互。
需要返回json数据
"""

# from django.contrib.auth.mixins import AccessMixin,LoginRequiredMixin
#方法一
# class LoginRequiredJSONMixin(AccessMixin):
#     """Verify that the current user is authenticated."""
#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return JsonResponse({'code':400,'errmsg':'用户未登录'})
#         return super().dispatch(request, *args, **kwargs)
#
# class Center(LoginRequiredJSONMixin,View):
#     def get(self,request):
#         return JsonResponse({'code':0,'errmsg':'OK'})

#方法二
# class LoginRequiredJSONMixin(LoginRequiredMixin):
#     def handle_no_permission(self):
#         return JsonResponse({'code':400,'errmsg':'用户未登录'})
# class Center(LoginRequiredJSONMixin,View):
#     def get(self,request):
#         return JsonResponse({'code':0,'errmsg':'OK'})

#以上两个人方法都可以，为了以后调用方便，单独放到utils的view_user文件中
from utils.view_user import LoginRequiredJSONMixin
class Center(LoginRequiredJSONMixin,View):
    def get(self,request):
        #request.user是来源于中间件，源码表示如果是已登录用户获取登录用户信息，如果不是，获取匿名用户信息（没有用户的ID、username等等）
        info_data = {
            'username':request.user.username,
            'email':request.user.email,
            'mobile':request.user.mobile,
            'email_active':request.user.email_active,
        }
        return JsonResponse({'code':0,'errmsg':'OK','info_data':info_data})

class Email(View):
    def put(self,request):
        data = json.loads(request.body.decode())
        email = data.get('email')
        if not email:
            return JsonResponse({'code':400,'errmsg':'参数不全'})
        if not re.match('^[a-z0-9][\w\\\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
            return JsonResponse({'code':400,'errmsg':'邮箱格式错误'})
        #获取登录用户
        login_user = request.user
        login_user.email = email
        login_user.save()


        # send_mail(subject=subject,
        #           message=html_message,
        #           from_email=from_email,
        #           recipient_list=recipient_list)

        verify_url = generic_email_verify_token(request.user)
        celery_send_mail.delay(email,verify_url)
        return JsonResponse({'code':0,'errmsg':'OK'})

class EmailsVerification(View):
    def put(self,request):
        params = request.GET
        token = params.get('token')
        if token is None:
            return JsonResponse({'code':400,'errmsg':'参数不全'})
        user_id = check_verifu_token(token)
        if user_id is None:
            return JsonResponse({'code':400,'errmsg':'参数错误'})
        user = User.objects.get(id=user_id)
        user.email_active = True
        user.save()
        return JsonResponse({'code':0,'errmsg':'OK'})