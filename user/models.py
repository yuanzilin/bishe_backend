from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    type = models.CharField(max_length=100, blank=True)
    invitation = models.CharField(max_length=100,blank=True)
    taskNumber=models.IntegerField(default=0)
    toolNumber=models.IntegerField(default=0)
    serviceNumber=models.IntegerField(default=0)
    qualified=models.IntegerField(default=0)

    class Meta(AbstractUser.Meta):
        pass
