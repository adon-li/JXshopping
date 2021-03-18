#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Liyd
# @Email   : muziyadong@gmail.com
# @Software: PyCharm

from django.urls import path
from apps.addrs.views import Areas,SubAreas

urlpatterns = [
    #users子应用的路由
    path('areas/',Areas.as_view()),
    path('areas/<city_id>/',SubAreas.as_view()),
]

