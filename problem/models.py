from django.db import models


# Create your models here.
# 每个问题有这几个属性：name，user，type，time_handle，time_limit
# 在这里统一说明一下status的取值
# 1：等待中
# 2：运行中
# 3：已完成
# 4：已终止
class Problem(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    subtype = models.CharField(max_length=100,default="")
    user_submit = models.CharField(max_length=30, default="")
    time_submit = models.DateTimeField(auto_now_add=True)
    time_limit = models.IntegerField(default=10)
    status = models.IntegerField(default=1)
    fileZip_url = models.CharField(max_length=30)
    fileSetting_url = models.CharField(max_length=30)
    result = models.TextField(default="")
    # celery执行该任务时的id号,和数据库中自动生成的id号不是一回事
    celery_id=models.CharField(max_length=100,default='')


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

# 这个表格是没用的了
TASK_STATUS = (
    (1, "等待中"),
    (2, "运算中"),
    (3, "已取消"),
    (4, "已完成"),
)
