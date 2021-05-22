import json

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse

from problem.models import Problem
from service.models import Service
from tool.models import Tool
from .models import *
from django.contrib import auth
from django import forms  # 导入表单
# from django.contrib.auth.models import User  # 导入django自带的user表
from django.contrib.sessions.models import Session
from .forms import UserForm_test


# Create your views here.
# 注册的用户表
class UserForm_r(forms.Form):
    type = forms.CharField(max_length=100)
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密码', max_length=100)
    email = forms.CharField(label='邮箱', max_length=100)
    invitation = forms.CharField(label='邀请码', max_length=100)


# 开发者的注册表
class DeveloperForm_r(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密码', max_length=100)
    email = forms.CharField(label='邮箱', max_length=100)
    invitation = forms.CharField(label='邀请码', max_length=100)


def register(request):
    if request.method == 'POST':
        uf = UserForm_r(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            email = uf.cleaned_data['email']
            Type = uf.cleaned_data['type']
            # 添加到数据库
            flag = User.objects.filter(type=Type).filter(username=username).count()
            if flag > 0:
                return JsonResponse({
                "code": 101,
                "username": username,
                "password": password,
                "email": email,
                "type": Type,
                "detail": "用户名已被使用"
                })
            else:
                if Type == "developer":
                    invitation = uf.cleaned_data['invitation']
                    User.objects.create_user(username=username, password=password, email=email, type=Type, invitation=invitation)
                    return JsonResponse({
                        "code": 102,
                        "username": username,
                        "password": password,
                        "email": email,
                        "type": Type,
                        "detail": "开发者注册成功"
                    })
                else:

                    User.objects.create_user(username=username, password=password, email=email, type=Type)
                    return JsonResponse({
                    "code": 102,
                    "username": username,
                    "password": password,
                    "email": email,
                    "type": Type,
                    "detail": "注册成功"
                    })


# 登录的表
class UserForm_l(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密码', max_length=100)
    type = forms.CharField(max_length=100)


# 登录
def login(request):
    if request.method == 'POST':
        uf_l = UserForm_l(request.POST)
        if uf_l.is_valid():
            type = uf_l.cleaned_data['type']
            username = uf_l.cleaned_data['username']
            password = uf_l.cleaned_data['password']
            # 用户认证
            re = auth.authenticate(username=username, password=password, type=type)

            if re.type == type or re.is_superuser==1:
                if type!="developer":
                    auth.login(request, re)  # 登录成功,这个login方法还可以把用户数据保存在session中
                    return JsonResponse({
                        "code": 202,
                        "username": username,
                        "password": password,
                        "detail": "登录成功!"
                    })
                elif re.qualified==0:
                    return JsonResponse({
                        "code": 204,
                        "username": username,
                        "password": password,
                        "detail": "该开发者账号尚未通过审核"
                    })
                elif re.qualified==2:
                    User.objects.filter(username=username,type="developer").delete()
                    return JsonResponse({
                        "code": 205,
                        "username": username,
                        "password": password,
                        "detail": "该开发者账号申请被拒"
                    })

                else:
                    return JsonResponse({
                        "code": 202,
                        "username": username,
                        "password": password,
                        "detail": "登录成功!"
                    })

            else:
                return JsonResponse({
                    "code": 201,
                    "username": username,
                    "password": password,
                    "detail": "用户名或密码错误"
                })
        else:
            return JsonResponse({
                "code": 203,
                "detail": "输入数据未通过校验！不合法"
            })


def logout(request):
    auth.logout(request)
    return JsonResponse({"detail": "您已退出登录"})


def getAllUser(request):
    type=request.GET.get('type')
    status=request.GET.get('status')
    if status=="-1":
        find_data=User.objects.filter(type=type).values()
        return_data={}
        return_data['data']=list(find_data)
        return JsonResponse(return_data)
    else:
        find_data = User.objects.filter(type=type,qualified=status).values()
        return_data = {}
        return_data['data'] = list(find_data)
        return JsonResponse(return_data)

def deleteUser(request):
    post_json = json.loads(request.body.decode('utf-8'))
    print("deleteTool,post_json=", post_json)
    id = post_json['id']
    type=post_json['type']
    print("168168,type=",type)
    result=User.objects.get(id=id)
    User.objects.get(id=id).delete()
    print("159,user-views,username=",result.username)
    if(type=="user"):
        Problem.objects.filter(user_submit=result.username).delete()
    if(type=="developer"):
        print("176176176,developer=",result.username)
        print("175175,deleteUser,tool=",Tool.objects.filter(tool_uploader=result.username))
        Tool.objects.filter(tool_uploader=result.username).delete()
        Service.objects.filter(developer=result.username).delete()
    return JsonResponse({
        "feedback": "success"
    })

def deleteDeveloper(request):
    pass

def reviewDeveloper(request):
    post_json=json.loads(request.body.decode('utf-8'))
    id=post_json['id']
    flag=post_json['flag']
    result=User.objects.get(type="developer",id=id)
    if(flag==1):
        result.qualified=1
    if(flag==2):
        result.qualified=2
    result.save()
    return JsonResponse({
        "feedback": "success"
    })

def logoutuser(request):
    post_json=json.loads(request.body.decode('utf-8'))
    print("post_json=",post_json)
    type=post_json["type"]
    username=post_json["username"]
    print("user-views.py,205,post_json=",post_json)
    if type == "developer":
        user = User.objects.get(type=type, username=username)
        user.delete()
    if type == "user":
        Problem.objects.filter(user_submit=username).delete()
        user=User.objects.get(type="user",username=username)
        user.delete()
    return JsonResponse({
        "feedback": "注销成功"
    })


def downloadSQL(request):
    import os
    print(os.getcwd())
    file = open('db.sqlite3', 'rb')
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
    response['Content-Disposition'] = 'attachment;filename="db.sqlite3"'
    return response


