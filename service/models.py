from django.db import models

# Create your models here.
class Service(models.Model):
    dev_time = models.DateTimeField(auto_now_add=True)
    service_name = models.CharField(max_length=100)
    developer = models.CharField(max_length=100)
    type = models.CharField(max_length=100,default="")
    service_file=models.CharField(max_length=100,default="")

class saveServiceFilePath(models.Model):
    create_time=models.DateTimeField(u"上传时间")
    file_url = models.FileField(upload_to='Service_file')
