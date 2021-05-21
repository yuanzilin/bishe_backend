import json
import os
from datetime import time
from time import localtime

from django.core import serializers
from django.core.files import File
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import viewsets

from djangoProject1.celery import app
from djangoProject1.settings import BASE_DIR
from problem.models import Problem, SaveFile, SaveProblemZip, SaveProblemSetting
from problem.serializer import ProblemSerializer
from django.utils import timezone

from service.models import Service
from user.models import User
from .forms import submitForm

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from .task import my_task, solveProblem


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
    return render_json({"path": "/ProblemZip/"+str(data)})


# 上传problem表单文件中的文件
def upload_problem_setting(request):
    data = request.FILES.get('file')
    print('-'*10, type(data))
    create_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    SaveProblemSetting.objects.create(create_time=create_time, file_url=data)
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

# 运行单参数的exe文件
def runexe_single(main,params):
    os.system(main+' '+params)

def run_cmd(cmd):
    result_str=os.popen(cmd).read()
    return result_str

# 获取任务文件和服务文件的相对路径
# 目前只支持单参数可执行文件
def splicefile_single(subtype,program):
    # 首先是根据subtype获取相应的可执行文件，把这个文件路径存到exe里面
    exe = Service.objects.filter(service_name=subtype)[0].service_file
    #
    ps = program.split('/')
    es = exe.split('/')

    p_cnt = 0
    for i in ps:
        p_cnt += 1

    e_cnt = 0
    for i in es:
        e_cnt += 1

    comps = ps[p_cnt - 2] + '\\' + ps[p_cnt - 1]
    comes = es[e_cnt - 2] + '\\' + es[e_cnt - 1]
    # 组合单参数命令
    cmd=comes+' '+comps
    # 把执行的结果存到字符串里
    str = os.popen(cmd).read()
    return str


# 存储表单数据并把任务加到异步队列中
def saveProblem(request):
    # import time
    # time.sleep(2)

    # 1.解析参数
    post_json=json.loads(request.body.decode('utf-8'))
    # 用户名
    user_submit=post_json['username']
    # 任务名
    name=post_json['problemName']
    # 运行上限
    time_limit=int(post_json['timeout'].replace('s',''))
    # 任务文件所在路径
    fileZip_url=post_json['Zips_file']
    # 任务配置文件路径
    fileSetting_url=post_json['settings_path']
    # 任务的提交时间
    time_submit = timezone.now().strftime("%Y-%m-%d %H:%M")
    # 服务的具体名称
    subtype=post_json['subtype']
    # 服务的大分类
    type = post_json['type']

    # 2.加入到任务队列中，开始异步调度
    # 获取任务id,从而控制该任务的终止和开始
    celery_id=solveProblem.delay(name,subtype,fileZip_url,time_limit)
    print("160160,problem-saveProblem.py")
    # 3.把数据加入到数据库中
    Problem.objects.create(user_submit=user_submit,
                           name=name,
                           time_limit=time_limit,
                           fileZip_url=fileZip_url,
                           fileSetting_url=fileSetting_url,
                           time_submit=time_submit,
                           subtype=subtype,
                           type=type,
                           celery_id=celery_id)
    user = User.objects.get(username=user_submit, type="user")
    user.taskNumber += 1
    user.save()


    # 4.返回
    return JsonResponse({
        "feedback":"提交任务成功"
    })

# 任务状态查询,,用post方式查询,查询的参数为'name'
# 1：等待中
# 2：运行中
# 3：已完成
# 4：已终止
def getTaskStatus(request):
    post_json=json.loads(request.body.decode('utf-8'))
    name=post_json['name']
    status=Problem.objects.get(name=name).status
    if status==1:
        return JsonResponse({
            "status":"等待中"
        })
    if status==2:
        return JsonResponse({
            "status":"运行中"
        })
    if status==3:
        return JsonResponse({
            "status":"已完成"
        })
    if status==4:
        return JsonResponse({
            "status":"已终止"
        })

# 任务终止
# 任务中止又分两种:一种是处在等待中的任务(status为1),一种是正在运行的(status为2)
# 用post发送过来的参数中,也是只需要把name发送过来
def terminateTask(request):

    post_json=json.loads(request.body.decode('utf-8'))
    task=Problem.objects.get(id=post_json['id'])
    '''
    这部分代码不要删，到后面可能要用来真正地终止任务的运行
    celery_id=task.celery_id
    from djangoProject1.celery import app
    from celery.app.control import Control
    app.control.revoke(str(celery_id),terminate=True)
    '''
    task.status=4
    task.save()
    return JsonResponse({
        "feedback":"中止成功"
    })

# 任务启动
def startTask(request):
    # 暂时不知道怎么做
    pass


# 获取所有的数据
def getProblemData(request):
    type = request.GET.get('type')
    username = request.GET.get('username')
    if type == "all":
        find_data = Problem.objects.filter(user_submit=username).values()
        print(find_data.all())
        return_data = {}
        return_data['data'] = list(find_data)
        return JsonResponse(return_data)
    else:
        find_data = Problem.objects.filter(type=type, user_submit=username).values()
        return_data = {}
        return_data['data'] = list(find_data)
        return JsonResponse(return_data)

# 根据任务ID获取任务数据
def getResultById(request):
    id = request.GET.get('id')
    find_data = Problem.objects.filter(id=id).values()
    return_data = {}
    return_data['data'] = list(find_data)
    return JsonResponse(return_data)


# 下载结果,这里也可以改一下,改成txt文件
def downloadResult(request):
    id = request.GET.get('id')
    find_data = Problem.objects.filter(id=id).values()
    result=find_data[0]["result"]
    print("207207207207",type(result))
    print("207,problemview-downloadresult",result)

    # 生成PDF文件
    # buffer = io.BytesIO()
    # p=canvas.Canvas(buffer)
    # textobject = p.beginText(50,750)
    # rs=result.split('\n')
    # for i in rs:
    #     textobject.textLine(i)
    # p.drawText(textobject)
    # p.showPage()
    # p.save()
    # buffer.seek(0)
    #
    # return FileResponse(buffer,as_attachment=True,filename='result.pdf')

    # 生成txt文件
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=result.txt'
    response.write(result)
    return response


def getTaskDataByStatus(request):
    status = request.GET.get('status')
    id=request.GET.get('id')
    if id=="0":
        # username = request.GET.get('username')
        find_data = Problem.objects.filter(status=status).values()
        print(find_data.all())
        return_data = {}
        return_data['data'] = list(find_data)
        return JsonResponse(return_data)
    else:
        user=User.objects.get(id=id)
        # print("248248248,gettaskDataByStatus,user=",user.username)
        find_data = Problem.objects.filter(status=status,user_submit=user.username).values()
        print(find_data.all())
        return_data = {}
        return_data['data'] = list(find_data)
        return JsonResponse(return_data)




# celery视图
def index(request):
    x=my_task.delay(3,4)
    return HttpResponse("<h1>服务器返回响应内容</h1>")

def deleteTask(request):
    post_json=json.loads(request.body.decode('utf-8'))
    print("319,deleteTask,post_json=",post_json)
    task=Problem.objects.get(id=post_json['id'])
    user=User.objects.get(username=task.user_submit)
    task.delete()
    user.taskNumber-=1
    user.save()
    return JsonResponse({
        "feedback":"删除任务成功"
    })


