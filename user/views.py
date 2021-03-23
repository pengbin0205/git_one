import random
import string

from django.db import transaction
from django.db.models import Q
from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.http import HttpResponse, response
from django_redis import get_redis_connection
from redis import Redis

from user.captcha.image import ImageCaptcha
# Create your views here.
from user.models import User
from user.utils.hash_code import hash_pwd, hash_email
from user.utils.salt import get_salt


def captcha(request):
    img = ImageCaptcha()
    cc = random.sample(string.ascii_letters + string.digits, 4)
    cc = "".join(cc)

    data = img.generate(cc)
    # 返回二进制数据

    request.session['captcha'] = cc
    return HttpResponse(data, "img/png")


def register(request):
    return render(request, "user/register.html")


def user_register(request):
    # 1. 获取前端传递的参数并判断参数是是否合法
    phone = request.POST.get("phone")
    email = request.POST.get("email")
    pwd = request.POST.get("user_pwd")
    sex = request.POST.get("sex")
    email_code = request.POST.get("email_code")
    if sex == 'm':
        sex = True
    else:
        sex = False
    # 2. 比对邮箱验证码是否一致

    # redis = Redis(host="192.168.92.128", port=7000)
    # code = redis.get(email)
    # redis.setex(email,300,code)
    # redis_connection = get_redis_connection("default")
    # code = redis_connection.get(email)

    # 如果code不存在，则代表验证码已过期
    code = request.session.get('code')
    if email_code != code:
        return HttpResponse("邮箱验证码不一致")
    # 3. 将用户的数据保存至数据库
    salt = get_salt()
    hash_password = hash_pwd(pwd, salt)
    number = request.POST.get('number')
    cc2 = request.session.get('captcha')
    number = number.lower()
    cc2 = cc2.lower()
    with transaction.atomic():
        if (number == cc2):
            user = User.objects.create(email=email, phone=phone, password=hash_password, sex=sex,salt=salt)
            if user:
                return redirect("/user/login")
        else:
            return HttpResponse('验证码错误')
    # 4. 如果对象保存成功，重定向到渲染登录页面的视图
    return redirect("user:login")


def send_email(request):
    request.session.flush()
    email = request.GET.get("email")
    subject = "欢迎您注册百知教育员工系统"
    # 随机验证码
    code = random.sample(string.digits,6)
    code = ''.join(code)
    # 在发送验证码时需要将验证码储存起来，方便注册时验证，并设置验证码的有效期
    if request.session.get('code'):
        del request.session['code']
    request.session['code'] = code
    # redis = Redis(host="192.168.92.128", port=7000)
    # redis.setex(email, 300, code)
    # redis_connection = get_redis_connection("default")
    # redis_connection.setex(email, 300, code)
    # request.session['code'] = code
    # 判断email以及email是否合法
    if email:
        status = send_mail(
            subject,
            f"这是您的注册码{code}，请在5分钟内完成注册",
            "3202448109@qq.com",
            [email],
        )
        if status:
            return HttpResponse("邮件发送成功")
    return HttpResponse("邮件发送失败，请稍等")


def login(request):
    try:
        name = request.COOKIES.get('name')
        pwd = request.COOKIES.get('pwd')
        with transaction.atomic():
            user = User.objects.filter(Q(email=name, password=pwd) | Q(phone=name, password=pwd)).first()
            if user:
                request.session['is'] = True
                request.session['name'] = name
                return redirect('http://127.0.0.1:8000/ems/index/')
            else:
                return render(request,"user/login.html")
    except:
        return render(request,"user/login.html")

def login2(request):
    try:
        name = request.POST['name']
        pwd = request.POST['pwd']
        check = request.POST.get('check')
        with transaction.atomic():
            user = User.objects.filter(Q(email=name) | Q(phone=name)).first()
            salt = user.salt
            # 再次对密码进行加密对比
            hash_pwd1 = hash_pwd(pwd, salt)
            user = User.objects.filter(Q(email=name, password=hash_pwd1) | Q(phone=name, password=hash_pwd1))
            if user:
                request.session['is'] = True
                request.session['name'] = name
                if check == '1':
                    response = redirect('http://127.0.0.1:8000/ems/index/')
                    response.set_cookie('name',name,max_age=3600 * 24 * 7)
                    response.set_cookie('pwd',hash_pwd1 ,max_age=3600 * 24 * 7)
                    return response
                else:
                    response = redirect('http://127.0.0.1:8000/ems/index/')
                    return response
            else:
                return HttpResponse('用户名或密码错误')
    except:
        return HttpResponse('登录失败')

def checkEmail2(request):
    email = request.POST.get('email')
    user = User.objects.filter(email=email)
    if user:
        return HttpResponse('邮箱已存在')
    else:
        return HttpResponse()

def checkPhone2(request):
    phone = request.POST.get('phone')
    user = User.objects.filter(phone=phone)
    if user:
        return HttpResponse('手机号已存在')
    else:
        return HttpResponse()

def check(request):
    # 1. 接收到前端的参数
    name = request.GET.get("name")

    # 2. 查询用户名是否已存在
    user_set = User.objects.filter(Q(email=name) | Q(phone=name))
    if user_set:
        return HttpResponse("用户名已存在")

    return HttpResponse("")