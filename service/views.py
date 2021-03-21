from django import forms
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

# Create your views here.
from service.models import Service, saveServiceFilePath


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
    if request.method == "POST" and request.POST:
        service_form = serviceForm(request.POST)
        if service_form.is_valid():
            service_name = service_form.cleaned_data["service_name"]
            type = service_form.cleaned_data["type"]
            developer = service_form.cleaned_data["developer"]
            service_file=service_form.cleaned_data["service_file"]
            dev_time = timezone.now().strftime("%Y-%m-%d %H:%M")
            Service.objects.create(service_name=service_name, type=type, developer=developer, dev_time=dev_time,service_file=service_file)
            return JsonResponse({
                "service_name": service_name,
                "type": type,
                "developer": developer,
                "dev_time": dev_time,
            })

def getData(request):
    type = request.GET.get('type')
    service_type = request.GET.get('service_type')
    if type == "1":
        # 开发者查询
        dev_name = request.GET.get('dev_name')
        find_data = Service.objects.filter(developer=dev_name,type=service_type).values()
        return_data = {}
        return_data['data'] = list(find_data)
        return JsonResponse(return_data)
    if type == "2":
        # 管理员查询
        pass
    if type == "3":
        # 用户获取数据
        find_data = Service.objects.filter(type=service_type).values()
        return_data = {}
        return_data['data'] = list(find_data)
        return JsonResponse(return_data)