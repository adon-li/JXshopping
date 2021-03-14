#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Liyd
# @Time : 2021/3/9 15:53
# @Email   : muziyadong@gmail.com
# @Software: PyCharm

from django.urls import path
from apps.verifications.views import ImageCode

urlpatterns = [
    #users子应用的路由
    path('image_codes/<uuid>/',ImageCode.as_view())
]
