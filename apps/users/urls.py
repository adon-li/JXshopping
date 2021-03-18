#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Liyd
# @Time : 2021/3/7 6:13
# @Email   : muziyadong@gmail.com
# @Software: PyCharm
from django.urls import path
from apps.users.views import UsernameCount,MobileCount,Register,\
    Login,Logout,Center,Email,EmailsVerification,\
    AddressCreate,Addresses,UpdateAddress,DefaultAddress,UpdateTitle,UpdatePassword
urlpatterns = [
    path('usernames/<username:username>/count/',UsernameCount.as_view()),
    path('mobiles/<mobile:mobile>/count/',MobileCount.as_view()),
    path('register/',Register.as_view()),
    path('login/',Login.as_view()),
    path('logout/',Logout.as_view()),
    path('info/',Center.as_view()),
    path('emails/',Email.as_view()),
    path('emails/verification/',EmailsVerification.as_view()),
    path('addresses/create/',AddressCreate.as_view()),
    path('addresses/',Addresses.as_view()),
    path('addresses/<address_id>/',UpdateAddress.as_view()),
    path('addresses/<address_id>/default/',DefaultAddress.as_view()),
    path('addresses/<address_id>/title/',UpdateTitle.as_view()),
    path('password/',UpdatePassword.as_view()),
]


