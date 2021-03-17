#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Liyd
# @Email   : muziyadong@gmail.com
# @Software: PyCharm
from django.views import View
from django.contrib.auth.mixins import AccessMixin,LoginRequiredMixin
from django.http import JsonResponse
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

class LoginRequiredJSONMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        return JsonResponse({'code':400,'errmsg':'用户未登录'})
# class Center(LoginRequiredJSONMixin,View):
#     def get(self,request):
#         return JsonResponse({'code':0,'errmsg':'OK'})



