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
class UsernameCount(View):
    def get(self,request,username):
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code':'0','count':count,'errmsg':'ok'})
