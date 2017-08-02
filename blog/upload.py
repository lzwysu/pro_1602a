#coding:utf8
#上传相关模块
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt # 不需要csrf验证
import json
import os
import datetime
from django.conf import settings
import uuid

@csrf_exempt
def upload_image(req,dirname):
    f = req.FILES.get('imgFile',None)

    res = {'error':1,'message':'上传错误'}
    if f:
        res = do_upload(f,dirname)
    return HttpResponse(json.dumps(res))

def do_upload(f,dirname):
    file_suffix = f.name.split('.')[-1] # 获取文件后缀名
    relative_path = create_dir(dirname)
    name = str(uuid.uuid1()) + '.' + file_suffix # 文件名
    fname = os.path.join(settings.MEDIA_ROOT,relative_path,name)
    #把文件写入服务器上
    with open(fname,'wb') as file:
        file.write(f.file.read())
    image_url = settings.MEDIA_URL + relative_path + name  # 告诉编辑器图片的url地址
    return {'error':0,'url':image_url}

#创建目录
def create_dir(dirname):
    today = datetime.datetime.today()
    dirname = dirname + '/%d/%d/' % (today.year,today.month) # kindeditor/年/月
    path = os.path.join(settings.MEDIA_ROOT ,dirname)
    if not os.path.exists(path):
        os.makedirs(path)
    return dirname
