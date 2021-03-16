#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Liyd
# @Email   : muziyadong@gmail.com
# @Software: PyCharm
from libs.yuntongxun.sms import CCP
from celery_work.main import celery_app
#函数必须用task装饰器装饰
@celery_app.task
def celery_send_sms_code(mobile,sms_code):
    #发动短信任务
    CCP().send_template_sms(mobile, [sms_code, 5], 1)


