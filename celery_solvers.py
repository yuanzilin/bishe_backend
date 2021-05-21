from __future__ import absolute_import,unicode_literals

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject1.settings')  # 设置django环境
django.setup()
# -------------------------------------------------
from celery import Celery
app = Celery("myapp")
app.config_from_object("celery_config1")

#from celery import shared_task

import time

#@shared_task
#def add(x,y):
#    return x+y

def mul(x,y):
    return x*y

@app.task
def my_task(x,y):
    print("x=",x,",y=",y)
    f = open("123",mode='w')
    f.write("x")
    f.close()

    print("任务开始执行")
    time.sleep(20)
    print("任务执行结束")


if __name__ == "__main__":
    os.system("celery -A celery_solvers worker --concurrency=4 --loglevel=INFO -P threads")