import json
import os
from datetime import time
from time import localtime

from django.core import serializers
from django.core.files import File
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import viewsets

from djangoProject1.settings import BASE_DIR
from problem.models import Problem, SaveFile, SaveProblemZip, SaveProblemSetting
from problem.serializer import ProblemSerializer
from django.utils import timezone
from .forms import submitForm


# Create your views here.
class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

# 尝试1：start
def render_json(data, status=200):
    return HttpResponse(json.dumps(data), content_type="text/json", status=status)


def download_excel(request):
    file_id = request.GET.get('id')
    print("-"*10, file_id)
    file_path = SaveFile.objects.filter(id=int(file_id)).values('file_url')[0]
    file_path = file_path.get('file_url')
    print(file_path, file_id)
    with open(file_path, "rb") as f:
        res = HttpResponse(f)
        res["Context-Type"] = "application/octet-stream"
        res["Context-Disposition"] = 'attachment;filename="{}"'.format(file_path)
        return res
# 尝试1：end


def download(request, filename):
    file_pathname = os.path.join('SaveExcel/', filename)

    with open(file_pathname, 'rb') as f:
        file = File(f)

        response = HttpResponse(file.chunks(),
                                content_type='APPLICATION/OCTET-STREAM')
        response['Content-Disposition'] = 'attachment; filename=' + filename
        response['Content-Length'] = os.path.getsize(file_pathname)

    return response


# 上传problem表单文件中的文件
def upload_problem_zip(request):
    data = request.FILES.get('file')
    print('-'*10, type(data))
    create_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    SaveProblemZip.objects.create(create_time=create_time, file_url=data)
    print("666666666666,path=", data)
    return render_json({"path": "/ProblemZip/"+str(data)})


# 上传problem表单文件中的文件
def upload_problem_setting(request):
    data = request.FILES.get('file')
    print('-'*10, type(data))
    create_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    SaveProblemSetting.objects.create(create_time=create_time, file_url=data)
    print("666666666666,path=", data)
    return render_json({"path": "/ProblemSetting/"+str(data)})


# 保存上传的表单数据
def get_post_json(request):
    postBodyStr = request.body.decode('utf-8')
    post_json = json.loads(postBodyStr)
    return post_json


def handle_post(request):
    if request.method == 'POST':
        post_json = get_post_json(request)
        id = post_json['id']
        # 处理
        return JsonResponse({
        })  # 返回的如果是数组那么需要加参数safe = False


# 存储表单数据
def saveProblem(request):
    if request.method == "POST" and request.POST:
        submit_form = submitForm(request.POST)
        if submit_form.is_valid():
            subtype = submit_form.cleaned_data["subtype"]
            username = submit_form.cleaned_data["username"]
            name = submit_form.cleaned_data["problemName"]
            type = submit_form.cleaned_data["type"]
            time_submit = timezone.now().strftime("%Y-%m-%d %H:%M")
            timeout = submit_form.cleaned_data["timeout"]
            status = "1"
            zip_path = submit_form.cleaned_data["zip_path"]
            settings_path = submit_form.cleaned_data["settings_path"]
            Problem.objects.create(subtype=subtype,user_submit=username, name=name, type=type, time_submit=time_submit, time_limit=timeout, status=status, fileZip_url=zip_path, fileSetting_url=settings_path)
            return JsonResponse({
                "problemName": name,
                "timeout": timeout,
                "type": type,
                "zip_path": zip_path,
                "settings_path": settings_path,
                "result": "success",
            })


# 获取test数据
def getProblemData(request):
    type = request.GET.get('type')
    username = request.GET.get('username')
    print(111188181818181818, type, username)
    if type == "all":
        find_data = Problem.objects.filter(user_submit=username).values()
        print(find_data.all())
        return_data = {}
        return_data['data'] = list(find_data)
        return JsonResponse(return_data)
    else:
        find_data = Problem.objects.filter(type=type, user_submit=username).values()
        print(find_data.all())
        return_data = {}
        return_data['data'] = list(find_data)
        return JsonResponse(return_data)


# 获取analyse数据
def getAnalyseData(request):
    pass


# 获取validate数据
def getValidate(request):
    pass