from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.shortcuts import redirect  # 重新定向模块
from .userform import UserForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from .models import myrecord
import os
import json
import datetime
from myrecord import models
import string
import random

from .DL_service import *


# Create your views here.
def register_request(request):
    print(request.user.username)
    hint_message = ''
    if request.method == 'POST':
        print("yes")
        print(request.POST)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if not username or username.isspace():
            hint_message = '用户名不能为空'
        elif not password or password.isspace():
            hint_message = '密码不能为空'
        else:

            if "login" in request.POST:
                print("to login")
                user = authenticate(username=username, password=password)
                if not User.objects.filter(username=username):
                    hint_message = "用户名不存在"
                elif User.objects.filter(username=username) and user is None:
                    hint_message = "密码错误"
                else:
                    if login_check(request):
                        if request.user.username == username:
                            # 同一个用户
                            hint_message = "已登录"
                            # return render(request, 'login&logon.html', {"hintmessage": hint_message})
                            return redirect("homepage/")
                            # 已登录情况下，该浏览器不会再出现homepage页面
                        else:
                            logout(request)
                            # 强制前一用户下线
                    # 建立session记录
                    print("login")
                    login(request, user)
                    response = HttpResponseRedirect("homepage")
                    return response
                    # 重定向跳转

            elif "register" in request.POST:
                print("to register")
                if User.objects.filter(username=username):
                    hint_message = '用户名已注册'
                else:
                    new_user = User.objects.create_user(username=username, password=password)
                    new_user.save()
                    hint_message = "注册成功,请登录"

    print(hint_message)
    return render(request, 'login&logon.html', {"hintmessage": hint_message})


def homepage_request(request):
    print(request.user.username)
    if not login_check(request):
        return redirect("http://127.0.0.1:8000/register/")
    username = request.user.username
    return render(request, 'homepage.html', {"username": username})


def img_process_request(request, op):
    print(request.user.username)
    if not login_check(request):
        return redirect("http://127.0.0.1:8000/register/")
    username = request.user.username
    op_title = ""
    op_discription = ""
    op_rule = ""
    if op == "1":
        op_title = '图像分类'
        op_description = "blaaaaaaaaaaaaaaaaaaaaaaaa"
        op_rule = "you should blaaaaaaaaa"
    elif op == "2":
        op_title = '对象检测'
        op_description = "blaaaaaaaaaaaaaaaaaaaaaaaa"
        op_rule = "you should blaaaaaaaaa"
    elif op == "3":
        op_title = '人脸识别'
        op_description = "blaaaaaaaaaaaaaaaaaaaaaaaa"
        op_rule = "you should blaaaaaaaaa"
    elif op == "4":
        op_title = '风格转换'
        op_description = "blaaaaaaaaaaaaaaaaaaaaaaaa"
        op_rule = "you should blaaaaaaaaa"

    return render(request, 'image_process.html',
                  {"username": username, "op_title": op_title, "op_description": op_description, "op_rule": op_rule})


def upload_img(request):
    if not login_check(request):
        return redirect("http://127.0.0.1:8000/register/")
    print("into_upload")
    print(request.method)
    print(request.POST.get('name'))
    print(request.FILES)
    print(request.get_raw_uri())
    img_obj = request.FILES.get('file_img')
    print(img_obj)
    new_record = myrecord()
    new_record.op = get_op_type(request.get_raw_uri()[-8])
    new_record.owner = request.user
    img_src = request.user.username + '_' + datetime.datetime.now().strftime('%Y_%m_%d&%H_%I_%S') + '.jpg'
    new_record.image_input = 'input/' + img_src
    if request.get_raw_uri()[-8] != 1:
        new_record.image_output = 'output/' + img_src
    new_record.save()
    print(new_record.image_input)
    with open('./media/input/' + img_src, 'wb+') as f:
        f.write(img_obj.read())
    input_src = './media/input/' + img_src
    output_src = './media/output/' + img_src
    rtn_str = ''
    if request.get_raw_uri()[-8] == '1':
        new_record.info_output = classify_image(input_src)
        new_record.save()
        rtn_str = '|'.join(['1', input_src[1:], new_record.info_output])
    elif request.get_raw_uri()[-8] == '2':
        detect_image(input_src, output_src)
        rtn_str = '|'.join([request.get_raw_uri()[-8], input_src[1:], output_src[1:]])
    elif request.get_raw_uri()[-8] == '3':
        face_detection(input_src, output_src)
        rtn_str = '|'.join([request.get_raw_uri()[-8], input_src[1:], output_src[1:]])
    elif request.get_raw_uri()[-8] == '4':
        select_number = 1
        if request.POST.get('select_number') and request.POST.get('select_number').isdigit():
            select_number = int(request.POST.get('select_number'))
        transfer_image(input_src, output_src, select_number)
        rtn_str = '|'.join([request.get_raw_uri()[-8], input_src[1:], output_src[1:]])
    # 操作序号|输入图片路径| 输出图片路径 | 输出文本
    return HttpResponse(rtn_str)


def logout_request(request):
    logout(request)
    return redirect("http://127.0.0.1:8000/register/")


def login_check(request):
    # 判断是否已登录
    sessionid = request.COOKIES.get('sessionid', None)
    if sessionid is None:
        return False
    print(sessionid)
    print(Session.objects.all())
    sess = Session.objects.filter(pk=sessionid)
    print(sess)
    print(request.user.username)
    if sess is not None:
        # if request.COOKIES.get('is_login','') != True:
        # 避免重复登陆：一个sessionid值对应一个会话
        return True
    return False


def database_request(request):
    sessionid = request.COOKIES.get('sessionid', None)
    if sessionid is None:
        return False
    limit = 4
    print(myrecord.objects.all().order_by())
    p = Paginator(myrecord.objects.filter(owner=request.user).order_by('-created_at'), limit)
    # 实例化一个分页对象;按时间近远排列
    page = request.GET.get('page')  # 获取页码
    # print('我是page------------',page)
    # print('我是id------------',primary_domain_id)
    if page:
        pass
    else:
        page = 1
    try:
        a_a = p.page(page)  # 获取某页对应的记录
        page1 = p.page(page)
        page_list = page1.object_list
    except PageNotAnInteger:  # 如果页码不是个整数
        a_a = p.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        a_a = p.page(p.num_pages)  # 取最后一页的记录

    return render(request, 'personal_database.html',
                  {'username': request.user.username, 'page_list': page_list, 'second_list_obj': a_a, 'p': p})


def get_op_type(number):
    if number == '1':
        return '图像分类'
    elif number == '2':
        return '对象检测'
    elif number == '3':
        return '人脸识别'
    elif number == '4':
        return '风格转换'


def delete_record(request):
    id_list = request.POST.getlist('id_list[]')
    print(request.POST)
    print(id_list)

    for each in id_list:
        print(os.path.abspath('.'))
        os.remove('media/' + myrecord.objects.get(id=int(each)).image_input.name)
        os.remove('media/' + myrecord.objects.get(id=int(each)).image_output.name)
        # 移除文件夹内图片
        myrecord.objects.get(id=each).delete()
        #删除记录
    return HttpResponse("ok")
