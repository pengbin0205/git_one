import os
from uuid import uuid4

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from ems.models import Employee, Department


def del_session(request):
    request.session.flush()
    return render(request,'user/login.html')

def adduser(request):
    dept_list = Department.objects.all()
    return render(request,'ems/add.html',{'dept_list':dept_list})

def adduser2(request):
    username = request.POST.get('name')
    age = request.POST.get('age')
    salary = request.POST.get('salary')
    img_head = request.FILES.get('photo')
    print(img_head)
    sex = request.POST.get('sex')
    dept = request.POST.get('dept')
    extend = os.path.splitext(img_head.name)[1]
    # 获取后缀名
    img_head.name = str(uuid4()) + extend
    # 重命名,对图片文件无规则命名
    age = int(age)
    emp = Employee.objects.create(name=username, age=age, salary=salary, photo=img_head,gender=sex,dept_id=dept)
    if emp:
        return redirect("http://127.0.0.1:8000/ems/index/")
    else:
        return HttpResponse('添加失败')

def deluser(request):
    id = request.GET.get('id')
    emp = Employee.objects.get(id=id)
    emp.delete()
    return redirect("http://127.0.0.1:8000/ems/index/")

def updateuser(request):
    id = request.GET.get('id')
    return render(request,'ems/update.html',{'id':id})

def updateuser2(request):
    id = request.GET.get('id')
    name = request.POST.get('name')
    age = request.POST.get('age')
    salary = request.POST.get('salary')
    age = int(age)
    emp = Employee.objects.get(id=id)
    emp.name = name
    emp.age = age
    emp.salary = salary
    emp.save()
    return redirect("http://127.0.0.1:8000/ems/index/")

from django.core.paginator import Paginator


def index(request):
    a = request.session.get('is')
    name = request.session.get('name')
    emp_list = Employee.objects.all()
    # 获取前端传递的参数，通过此参数决定获取第几页的数据
    number = int(request.GET.get("number", 1))
    # 初始化一个分页器对象
    paginator = Paginator(object_list=emp_list, per_page=2)
    # 获取页面对象
    page = paginator.page(number)
    if a:
            return render(request,'ems/index.html',{'name':name,'page':page})
    else:
        return redirect('/user/login')

