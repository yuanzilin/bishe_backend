import json

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
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
            if re.type == type:
                auth.login(request, re)  # 登录成功,这个login方法还可以把用户数据保存在session中
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


# 用session实现登录功能
def login_session(request):
    if request.method == 'POST':
        uf_l = UserForm_l(request.POST)
        if uf_l.is_valid():
            username = uf_l.cleaned_data['username']
            password = uf_l.cleaned_data['password']
            try:
                get_user = User.objects.get(username=username)
                if get_user:
                    if(get_user.username==username and get_user.password==password):
                        session_list = []  # session列表
                        for se in session_list:
                            if get_user.username==se['username']:
                                Session.objects.filter(session_key=se.session['session_key'])
                                break
                        request.session['username']=get_user['username']
                        request.session['password']=get_user['password']
                        status = 1
                else:
                    pass
            except:
                pass