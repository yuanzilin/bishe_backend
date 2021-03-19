from django.db import models


# Create your models here.
# 每个问题有这几个属性：name，user，type，time_handle，time_limit
class Problem(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    subtype = models.CharField(max_length=100,default="")
    user_submit = models.CharField(max_length=30, default="")
    time_submit = models.DateTimeField(auto_now_add=True)
    time_limit = models.CharField(max_length=30)
    status = models.CharField(max_length=30)
    fileZip_url = models.CharField(max_length=30)
    fileSetting_url = models.CharField(max_length=30)


# 保存文件
class SaveFile(models.Model):
    create_time = models.DateTimeField(u"上传时间")
    file_url = models.FileField(upload_to='SaveExcel')  # 'SaveExcel'是保存excel的文件夹（即路径）


class SaveProblemZip(models.Model):
    create_time = models.DateTimeField(u"上传时间")
    file_url = models.FileField(upload_to='ProblemZip')


class SaveProblemSetting(models.Model):
    create_time = models.DateTimeField(u"上传时间")
    file_url = models.FileField(upload_to='ProblemSetting')


TASK_STATUS = (
    (1, "等待中"),
    (2, "运算中"),
    (3, "已取消"),
    (4, "已完成"),
)
