#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Liyd
# @Email   : muziyadong@gmail.com
# @Software: PyCharm
from django.core.mail import send_mail
from celery_work.main import celery_app
@celery_app.task
def celery_send_mail(email,verify_url):
    subject = '京西商城邮箱验证'
    from_email = 'fortunatedong@163.com'
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用京西商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (email, verify_url, verify_url)
    recipient_list = ['fortunatedong@163.com']

    send_mail(subject=subject,
              message='',
              html_message=html_message,
              from_email=from_email,
              recipient_list=recipient_list)

