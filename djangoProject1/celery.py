#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author:wd
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

from djangoProject1 import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject1.settings')  # 设置django环境

app = Celery('djangoProject1')

app.config_from_object('celery_config1')

app.autodiscover_tasks(settings.INSTALLED_APPS)  # 发现任务文件每个app下的task.py

# if __name__=='__main__':
#       app.start()

# if __name__ == "__main__":
#     os.system("celery -A djangoProject1 worker --concurrency=4 --loglevel=INFO -P threads")