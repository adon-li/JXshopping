#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Liyd
# @Email   : muziyadong@gmail.com
# @Software: PyCharm

from django.urls import path
from apps.goods.views import Index

urlpatterns = [
    #users子应用的路由
    path('index/',Index.as_view()),

]

