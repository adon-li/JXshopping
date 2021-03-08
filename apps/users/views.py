

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
from django.http import JsonResponse
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
        try:
            user = User.objects.create_user(username=username,password=password,mobile=mobile)
        except Exception as e:
            return JsonResponse({'code':400,'errmsg':'注册失败！'})
        return JsonResponse({'code':400,'errmsg':'注册成功！'})