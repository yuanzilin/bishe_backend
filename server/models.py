from django.db import models

# Create your models here.
class Server(models.Model):
    address = models.CharField(max_length=100)
    taskNum = models.IntegerField(default=0)
