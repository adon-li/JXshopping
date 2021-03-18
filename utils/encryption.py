#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Liyd
# @Email   : muziyadong@gmail.com
# @Software: PyCharm
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from JXshopping import settings
def generic_email_verify_token(user):
    s = Serializer(secret_key=settings.SECRET_KEY,expires_in=3600*24)
    data = ({'user_id':user.id,'email':user.email})
    token = s.dumps(data).decode()
    url = 'http://www.jx.com:8080/success_verify_email.html'
    verify_url = url + '?token=' + token
    return verify_url

def check_verifu_token(token):
    s = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600 * 24)
    try:
        result = s.loads(token)
    except Exception as e:
        return None
    return result.get('user_id')

