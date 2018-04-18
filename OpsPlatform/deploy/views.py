# -*- coding:utf-8 -*-

from django.shortcuts import render,HttpResponse
import os,time,subprocess
from .forms import GameInfoForm
from utils.paramiko_handle import Task
import json

# Create your views here.


def handle_upload_file(file,filename,path):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path+filename,'wb+')as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def pkg_unzip(name,path):
    md5_res = {}
    pkg = path + '/%s' % name
    if os.path.exists(path):
        os.system('rm -rf %s' % path)
    os.makedirs(path)
    os.system('unzip %s -d %s' % (name, path))
    for p,d,f in os.walk(path):
        for filename in f:
            md5 = subprocess('md5sum %s' % os.path.join(p, filename))
            md5_res[filename] = md5.split()[0]

    return md5_res

def upload(request):
    if request.method == "POST":
        path = 'static/upload/' + time.strftime('%Y-%m-%d-%H%M%S/')
        handle_upload_file(request.FILES['file'], str(request.FILES['file']),path)

        return HttpResponse('Successful')  #

    return render(request,'deploy/deploy.html')

def index(request):
    if request.method == 'GET':
        form = GameInfoForm()
        return render(request, 'deploy/index.html', {'form': form})

    elif request.method == 'POST':
        form = GameInfoForm(request.POST)
        if form.is_valid():
            obj = Task(request)
            result = obj.run()
            return HttpResponse(json.dumps(result))
























