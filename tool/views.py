from django import forms
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone



# Create your views here.
from tool.models import SaveToolPath, Tool


class submitForm(forms.Form):
    tool_uploader = forms.CharField(max_length=100)
    toolname = forms.CharField(max_length=100)
    toolversion = forms.CharField(max_length=100)
    toolpath = forms.CharField(max_length=100)


def uploadTool(request):
    data = request.FILES.get('file')
    print('-' * 10, type(data))
    create_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    SaveToolPath.objects.create(create_time=create_time, file_url=data)
    print("666666666666,path=", data)
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
            status = "1"
            Tool.objects.create(tool_uploader=tool_uploader, toolname=toolname, toolpath=toolpath, submit_time=submit_time, version=toolversion)
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
    print("type=",type)
    if type == "1":
        # 开发者查询
        find_data = Tool.objects.filter(tool_uploader=dev_name).values()
        print(find_data.all())
        return_data = {}
        return_data['data'] = list(find_data)
        return JsonResponse(return_data)
    if type == "2":
        # 管理员查询
        pass