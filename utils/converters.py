#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Liyd
# @Time : 2021/3/7 7:51
# @Email   : muziyadong@gmail.com
# @Software: PyCharm

class UsernameConverter:
    # 变量名必须为'regex',否则会找不到定义的字符窜规则
    regex = '[a-zA-Z0-9_-]{5,20}'
    def to_python(self,value):
        return value
class MobileConverter:
    regex = '1[3-9]\d{9}'
    def to_python(self,value):
        return str(value)

