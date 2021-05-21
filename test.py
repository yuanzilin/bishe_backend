from celery_solvers import my_task

x = my_task.delay(3, 4)
print("x=", x)