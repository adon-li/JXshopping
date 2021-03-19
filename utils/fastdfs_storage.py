#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Liyd
# @Email   : muziyadong@gmail.com
# @Software: PyCharm
from django.core.files.storage import Storage

class MyStorage(Storage):
    #创建存储类必须要实现_open()和_save()方法
    def _open(self,name,mode='rb'):
        pass
    def _save(self,name,content,max_length=None):
        pass
    #定义我们需要的方法，拼接链接调用fastdfs的数据
    def url(self, name):
        return "http://192.168.17.11:8888/"+name



