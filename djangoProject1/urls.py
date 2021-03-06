"""djangoProject1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from problem import views
from django.conf.urls import url
from django.urls import re_path


urlpatterns = [
    path('admin', admin.site.urls),
    path('api', include('problem.urls')),
    path('upload_problemZip', views.upload_problem_zip),
    path('upload_problemSetting', views.upload_problem_setting),
    path('download_excel', views.download_excel),
    path('download_result',views.downloadResult),
    path('submitForm', views.saveProblem),
    re_path('^getData/$', views.getProblemData),
    re_path('^getResultById/$', views.getResultById),
    re_path('^getTaskDataByStatus/$',views.getTaskDataByStatus),
    path('user/', include('user.urls')),
    path('tool/', include('tool.urls')),
    path('service/', include('service.urls')),
    url(r'^$', views.index),
    path('terminateTask', views.terminateTask),
    path('deleteTask', views.deleteTask),
    path('server/', include('server.urls')),

]
