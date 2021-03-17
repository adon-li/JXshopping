#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Liyd
# @Time : 2021/3/17 14:20
# @Email   : muziyadong@gmail.com
# @Software: PyCharm
from django.urls import path,include
from apps.oauth_login.views import QQLogin,OauthQQ
urlpatterns = [
    path('qq/authorization/',QQLogin.as_view()),
    path('oauth_callback/',OauthQQ.as_view()),
]


