import os
import time
import datetime

from djangoProject1.celery import app
from problem.models import Problem
from service.models import Service
from tool.models import Tool


@app.task
def my_task(x,y):
    print("x=",x,",y=",y)
    # f = open("123",mode='w')
    # f.write("x")
    # f.close()
    print("任务开始执行")
    time.sleep(20)
    print("任务执行结束")
    return x+y

# 解析类似这样的路径:http://127.0.0.1:8000/ProblemSetting/WA.txt
# 即文件路径为:服务器地址+文件夹+文件名
# 并把它做成python可以读取的样子
def parsingPath(path):
    ps=path.split('/')
    p_cnt=0
    for i in ps:
        p_cnt+=1
    combine_ps=ps[p_cnt-2]+'\\'+ps[p_cnt-1]
    return combine_ps

# 在这里进行任务的运算
# status的取值及含义如下
# 1：等待中
# 2：运行中
# 3：已完成
# 4：已终止
@app.task
def solveProblem(name, subtype, fileZip_url, time_limit):
    # name：任务的名字
    # subtype：该任务所选用的服务
    # fileZip_url：任务文件所处的位置
    # time_limit：运行上限

    # 先找到这个任务
    print("474747,name=",name)
    task = Problem.objects.get(name=name)

    # 让它睡10秒钟，当作是等待状态
    time.sleep(10)
    print("wait")


    # 先获取当前时间,然后开始运行
    t1=datetime.datetime.now()

    # 每一次修改任务状态前，都先检查一遍状态是否已经终止了，如果终止就直接退出
    if Problem.objects.get(name=name).status == 4:
        return
    print("status=", Problem.objects.get(name=name).status)
    status = 2
    task.status = status
    task.save()

    time.sleep(10)
    # 由于目前的服务都是一下子出结果,所以就只能依靠这个来展示一下任务进度了

    if (datetime.datetime.now()-t1).seconds>=time_limit:
        # 如果超时了,那就直接break,不进行下一步了
        status = 4
        task.status=status
        task.save()
        return

        # 根据subtype找到服务所需的参数
        # 还需要根据工具名去找对应的工具
    service = Service.objects.get(service_name=subtype)
    tool = Tool.objects.get(toolname=service.service_tool)
    # 解析任务文件路径
    service_args=service.service_args
    toolpath=parsingPath(tool.toolpath)
    taskFile=parsingPath(fileZip_url)
    print("service_args=", service_args)
    print("taskFile=", taskFile)
    # 执行
    cmd = service_args+' '+toolpath+' '+taskFile
    # os.system(cmd)
    result=os.popen(cmd).read()
    # print(result)

    # 每一次修改任务状态前，都先检查一遍状态是否已经终止了，如果终止就直接推出
    if Problem.objects.get(name=name).status == 4:
        return
    # 把结果存到数据库里
    task.status=3
    task.result=result
    task.save()

