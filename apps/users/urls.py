#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Liyd
# @Time : 2021/3/7 6:13
# @Email   : muziyadong@gmail.com
# @Software: PyCharm
from django.urls import path
from apps.users.views import UsernameCount
urlpatterns = [
    path('usernames/<username>/count/',UsernameCount.as_view()),
]


