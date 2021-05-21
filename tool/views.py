import json
import os

from django import forms
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone



# Create your views here.
from tool.models import SaveToolPath, Tool
from user.models import User


class submitForm(forms.Form):
    tool_uploader = forms.CharField(max_length=100)
    toolname = forms.CharField(max_length=100)
    toolversion = forms.CharField(max_length=100)
    toolpath = forms.CharField(max_length=100)
    toolDetail=forms.CharField(max_length=100)


def uploadTool(request):
    data = request.FILES.get('file')
    create_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    SaveToolPath.objects.create(create_time=create_time, file_url=data)
    return JsonResponse({
                "path": "/Tool_upload/" + str(data)
            })


def saveTool(request):
    if request.method == "POST" and request.POST:
        submit_form = submitForm(request.POST)
        if submit_form.is_valid():
            tool_uploader = submit_form.cleaned_data["tool_uploader"]
            toolname = submit_form.cleaned_data["toolname"]
            toolpath = submit_form.cleaned_data["toolpath"]
            submit_time = timezone.now().strftime("%Y-%m-%d %H:%M")
            toolversion = submit_form.cleaned_data["toolversion"]
            toolDetail=submit_form.cleaned_data["toolDetail"]
            status = "1"
            Tool.objects.create(toolDetail=toolDetail,tool_uploader=tool_uploader, toolname=toolname, toolpath=toolpath, submit_time=submit_time, version=toolversion)
            developer=User.objects.get(username=tool_uploader)
            developer.toolNumber+=1
            developer.save()
            return JsonResponse({
                "tool_uploader": tool_uploader,
                "toolname": toolname,
                "toolpath": toolpath,
                "submit_time": submit_time,
                "toolversion": toolversion,
                "result": "success",
            })

def getData(request):

    dev_name = request.GET.get('dev_name')
    type = request.GET.get('type')
    if type == "1" and dev_name==None:
        # 管理员查询
        find_data = Tool.objects.values()
        return_data = {}
        return_data['data'] = list(find_data)
        return JsonResponse(return_data)
    if type=="1" and dev_name!=None:
        # 管理员挨个查看
        find_data = Tool.objects.filter(tool_uploader=dev_name).values()
        return_data = {}
        return_data['data'] = list(find_data)
        return JsonResponse(return_data)
    if type == "2" and dev_name == 'all':
        # 开发者查询
        find_data = Tool.objects.values()
        return_data = {}
        return_data['data'] = list(find_data)
        return JsonResponse(return_data)
    if type == "2" and dev_name!=None:
        # 开发者查看自己上传的工具
        find_data = Tool.objects.filter(tool_uploader=dev_name).values()
        return_data = {}
        return_data['data'] = list(find_data)
        return JsonResponse(return_data)

def get_post_json(request):
    postBodyStr=request.body.decode('utf-8')
    post_json=json.loads(postBodyStr)
    return post_json

def getFilePath(str):
    list=str.split('/')
    len=0
    for i in list:
        len+=1
    filePath=list[len-2]+'\\'+list[len-1]
    return filePath

def deleteTool(request):
    post_json=json.loads(request.body.decode('utf-8'))
    print("deleteTool,post_json=",post_json)
    id=post_json['id']
    print("tool-views,66,id=", id)
    result=Tool.objects.filter(id=id).values()
    file_path=result[0]["toolpath"]
    Tool.objects.filter(id=id).delete()
    os.remove(getFilePath(file_path))
    return JsonResponse({
        "feedback":"success"
    })

def updateTool(request):
    post_json=json.loads(request.body.decode('utf-8'))
    id=post_json['id']
    result=Tool.objects.get(id=id)
    os.remove(getFilePath(result.toolpath))
    result.toolpath=post_json['toolpath']
    result.version=post_json['version']
    result.save()
    return JsonResponse({
        "feedback":"success"
    })
