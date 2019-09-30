import re
import requests
from .models import myrecord
import datetime
import os
from .DL_service import *


def get_image_list(url):
    try:
        page = requests.get(url).text
    except:
        return []
    image_list = []
    images = re.finditer(r'img src=\"(.+?\.jpg)', page)
    for image in images:
        image_list.append(image.group(1))
    return image_list


def download_image(url, username):

    img = requests.get(url)
    filename = url.strip().split('/')[-1]
    filename = username + '_' + datetime.datetime.now().strftime('%Y_%m_%d&%H_%I_%S') + '_' + filename
    input_src = './input/' + filename
    output_src = './output/' + filename
    with open(input_src, 'wb') as f:
        f.write(img.content)
        f.close()
    with open(output_src, 'wb') as f:
        f.close()
    return filename


def get_op_type(number):
    if number == '1':
        return '图像分类'
    elif number == '2':
        return '对象检测'
    elif number == '3':
        return '人脸识别'
    elif number == '4':
        return '风格转换'


def single_image_process(request, url):
    username = request.user.username
    img_src = download_image(url, username)
    input_src = './input/' + img_src
    output_src = './output/' + img_src
    new_record = myrecord()
    new_record.op = get_op_type(request.get_raw_uri()[-8])
    new_record.owner = request.user
    new_record.image_input = input_src
    if request.get_raw_uri()[-8] != 1:
        new_record.image_output = output_src
    new_record.save()
    print(new_record.image_input)
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
    rtn_list = []
    rtn_list.append(rtn_str)
    return rtn_list


def http_image_process(request, url):
    if url.split('.')[-1] == 'jpg':
        return single_image_process(request, url)
    image_list = get_image_list(url)
    username = request.user.username
    rtn_list = []
    for image in image_list:
        img_src = download_image(image, username)
        input_src = './input/' + img_src
        output_src = './output/' + img_src
        new_record = myrecord()
        new_record.op = get_op_type(request.get_raw_uri()[-8])
        new_record.owner = request.user
        new_record.image_input = input_src
        if request.get_raw_uri()[-8] != 1:
            new_record.image_output = output_src
        new_record.save()
        print(new_record.image_input)
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
        rtn_list.append(rtn_str)
    return rtn_list
