from django.db import models

# Create your models here.
class Service(models.Model):
    type = models.CharField(max_length=100,default="")
    dev_time = models.DateTimeField(auto_now_add=True)
    # 服务名词
    service_name = models.CharField(max_length=100)
    # 服务的开发者
    developer = models.CharField(max_length=100)
    # 服务的文件
    service_file=models.CharField(max_length=100,default="")
    # 服务的说明
    service_intro=models.TextField(default="")
    # 服务用到的工具，后面可能可以写成列表的形式
    service_tool=models.CharField(max_length=100,default="")
    # 服务所用的参数
    service_args=models.CharField(max_length=100,default="")



class saveServiceFilePath(models.Model):
    create_time=models.DateTimeField(u"上传时间")
    file_url = models.FileField(upload_to='Service_file')
