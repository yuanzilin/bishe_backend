from django.db import models

# Create your models here.
class Tool(models.Model):
    submit_time = models.DateTimeField(auto_now_add=True)
    tool_uploader = models.CharField(max_length=100)
    version = models.CharField(max_length=100)
    toolname = models.CharField(max_length=100)
    toolpath = models.CharField(max_length=100)
    # services = models.CharField(max_length=100)
    toolDetail=models.TextField(default="")


class SaveToolPath(models.Model):
    create_time = models.DateTimeField(u"上传时间")
    file_url = models.FileField(upload_to='Tool_upload')