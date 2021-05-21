import json

from django import forms
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

# Create your views here.
from service.models import Service, saveServiceFilePath
from user.models import User


def uploadService(request):
    pass

# 保存服务的类
class serviceForm(forms.Form):
    service_name=forms.CharField(max_length=100)
    type = forms.CharField(max_length=100)
    developer=forms.CharField(max_length=100)
    service_file=forms.CharField(max_length=100)

# 保存服务的配置文件
def saveServiceFile(request):
    data = request.FILES.get('file')
    create_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    saveServiceFilePath.objects.create(create_time=create_time,file_url=data)
    return JsonResponse({
        "path": "/Service_file/"+str(data)
    })

# 提交服务的相关信息
def submitService(request):
    post_json=json.loads(request.body.decode('utf-8'))
    dev_time = timezone.now().strftime("%Y-%m-%d %H:%M")
    service_name=post_json['service_name']
    service_intro=post_json['service_intro']
    service_args=post_json['service_args']
    service_tool=post_json['service_tool'][0]
    service_file=post_json['service_file']
    service_developer = post_json['service_developer']
    type=post_json['type']
    developer = User.objects.get(type="developer",username=service_developer)
    developer.serviceNumber += 1
    developer.save()
    Service.objects.create(service_name=service_name,
                           service_intro=service_intro,
                           service_args=service_args,
                           service_tool=service_tool,
                           service_file=service_file,
                           developer=service_developer,
                           dev_time=dev_time,
                           type=type)
    return JsonResponse({
        "service_name":service_name,
        "service_developer":service_developer,
        "feedback":"操作成功"
    })

    # if request.method == "POST" and request.POST:
    #     service_form = serviceForm(request.POST)
    #     if service_form.is_valid():
    #         service_name = service_form.cleaned_data["service_name"]
    #         type = service_form.cleaned_data["type"]
    #         developer = service_form.cleaned_data["developer"]
    #         service_file=service_form.cleaned_data["service_file"]
    #         Service.objects.create(service_name=service_name, type=type, developer=developer, dev_time=dev_time,service_file=service_file)
    #         return JsonResponse({
    #             "service_name": service_name,
    #             "type": type,
    #             "developer": developer,
    #             "dev_time": dev_time,
    #         })

def getData(request):
    type = request.GET.get('type')
    print("5252,service-getData,type=",type)
    service_type = request.GET.get('service_type')
    id=request.GET.get('id')
    if type == "2":
        # 管理员查询
        find_data = Service.objects.filter(type=service_type).values()
        return_data = {}
        return_data['data'] = list(find_data)
        return JsonResponse(return_data)
        pass
    if type == "3":
        # 用户获取数据
        find_data = Service.objects.filter(type=service_type).values()
        return_data = {}
        return_data['data'] = list(find_data)
        return JsonResponse(return_data)

    if type == "1" and id == "-1":
        # 开发者查询
        dev_name = request.GET.get('dev_name')
        find_data = Service.objects.filter(developer=dev_name,type=service_type).values()
        return_data = {}
        return_data['data'] = list(find_data)
        return JsonResponse(return_data)

    # 这个分支，是管理员查看开发者的服务列表，前端逻辑是传入开发者的id号，所以会修改id为正整数
    if id!="-1":
        dev_name=User.objects.get(id=id).username
        find_data = Service.objects.filter(developer=dev_name, type=service_type).values()
        return_data = {}
        return_data['data'] = list(find_data)
        return JsonResponse(return_data)


def deleteService(request):
    post_json=json.loads(request.body.decode('utf-8'))
    id=post_json['id']
    print("77777,service-views=",id)
    result=Service.objects.get(id=id)
    username=result.developer
    result_user=User.objects.get(username=username,type="developer")
    result_user.serviceNumber-=1
    result_user.save()
    Service.objects.filter(id=id).delete()
    return JsonResponse({
        "feedback":"删除成功"
    })

def getServiceIntro(request):
    service_name=request.GET.get('service_name')
    service=Service.objects.get(service_name=service_name)
    result={}
    result['data']=service.service_intro
    return JsonResponse(result)