#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Liyd
# @Email   : muziyadong@gmail.com
# @Software: PyCharm

import os
from celery import Celery
#配置环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "JXshopping.settings")
#实例化
celery_app = Celery('celery_work')
#加载配置配置文件，broker
celery_app.config_from_object("celery_work.config")
#自动检测指定包的任务
celery_app.autodiscover_tasks(['celery_work.SMS'])