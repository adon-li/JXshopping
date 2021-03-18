import re

from django.shortcuts import render

# Create your views here.
from pymysql import DatabaseError

from apps.users.models import User

"""
生成用户连接：
用户点击QQ图标，前端发送Ajax请求
调用QQLoginTool，生成跳转链接
响应返回json  
"""


from django.views import View
from QQLoginTool.QQtool import OAuthQQ
from django.http import JsonResponse
from apps.oauth_login.models import OauthQQUser
from django.contrib.auth import login
from django_redis import get_redis_connection
import json
class QQLogin(View):
    def get(self,request):
        qq = OAuthQQ(client_id = '101474184',
        client_secret =  'c6ce949e004e12ecc909ae6a8b09b637c',
        redirect_uri = 'http://www.jx.com:8080/oauth_callback.html',
        state = 'abc')
        qq_login_url = qq.get_qq_url()
        return JsonResponse({'code':0,'errmsg':'OK','login_url':qq_login_url})

class OauthQQ(View):
    def get(self,request):
        code = request.GET.get('code')
        if code is None:
            return JsonResponse({'code':400,'errmsg':'参数不全'})
        qq = OAuthQQ(client_id='101474184',
                     client_secret='c6ce949e004e12ecc909ae6a8b09b637c',
                     redirect_uri='http://www.jx.com:8080/oauth_callback.html',
                     state='abc')
        token = qq.get_access_token(code)
        openid = qq.get_open_id(token)
        #根据openid查询数据库是否已经存在
        try:
            qq_user = OauthQQUser.objects.get(openid=openid)
        except OauthQQUser.DoesNotExist:
            #如果没有绑定用户
            response = JsonResponse({'code':400,'access_token':openid})
            return response
        else:
            #如果绑定了用户，让其登录
            login(request,qq_user.user)
            response = JsonResponse({'code':0,"errmsg":'OK'})
            response.set_cookie('username',qq_user.user.username)
            return response

    def post(self,request):
        data = json.loads(request.body.decode())
        mobile = data.get('mobile')
        password = data.get('password')
        sms_code = data.get('sms_code')
        openid= data.get('access_token')

        #校验参数
        if not all([mobile,password,sms_code,openid]):
            return JsonResponse({'code':400,'errmsg':'参数不全'})
        if not re.match('^1[345789]\d{9}', mobile):
            return JsonResponse({'code': 400, 'errmsg': '手机号不满足规则'})
        if not re.match('[a-zA-Z0-9_-]{8,20}', password):
            return JsonResponse({'code': 400, 'errmsg': '密码不满足规则'})
        #检验短信验证码
        redis_conn = get_redis_connection('code')
        sms_code_redis = redis_conn.get('sms_%s'%mobile)
        if sms_code != sms_code_redis.decode():
            return JsonResponse({'code': 400,'errmsg': '输入的验证码有误'})
        #保存用户信息
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            user = User.objects.create_user(username=mobile,password=password,mobile=mobile)
        else:
            if not user.check_password(password):
                return JsonResponse({'code':400,'errmsg':'输入密码不正确'})
        #绑定openid
        try:
            OauthQQUser.objects.create(openid=openid,username=user)
        except DatabaseError:
            return JsonResponse({'code':400,'errmsg':'添加数据库数据错误'})
        #实现状态保持
        login(request,user)
        response = JsonResponse({'code':0,'errmsg':'OK'})
        response.set_cookie('username',user.username,max_age=3600*24*24)
        return response

