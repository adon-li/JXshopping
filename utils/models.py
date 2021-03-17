#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Liyd
# @Email   : muziyadong@gmail.com
# @Software: PyCharm
from django.db import models
class BaseModel(models.Model):
    #这是一个基类，方便其他model继承它
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')

    class Meta:
        #说明这是一个抽象模型类，数据库迁移时不会创建这个表，用于继承
        abstract = True


