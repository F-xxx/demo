from django.shortcuts import render,get_object_or_404,redirect
from .form import LoginForm,RegisterForm,UserModelForm
import json
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.decorators import login_required
from .models import Audit,User_Profile
from assets.models import Asset
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required
from io import BytesIO
from utils.verify_code import create_validate_code
from .custom_auth import UserManager

# Create your views here.

def check_code(request):
    stream = BytesIO()
    img,code = create_validate_code()
    img.save(stream,'pNG')
    request.session['verify_code'] = code
    return HttpResponse(stream.getvalue())

def login_ip(request):
    '''获取用户登陆地址'''
    ip_addr = ''
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip_addr = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip_addr = request.META['REMOTE_ADDR']
    return ip_addr

def login_view(request):
    if request.method == 'GET':
        return render(request,'login.html')
    elif request.method == 'POST' and request.is_ajax():
        result = {'status':False,'message':None}
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None and user.is_active:
                print(form.cleaned_data)
                result['status'] = True
                login(request,user)
                user_info = User_Profile.objects.filter(email=user).values('id', 'email').first()
                request.session['user_info'] = user_info
                Audit.objects.create(type='用户登录',
                                     user=request.user,
                                     action='登录',
                                     action_ip=login_ip(request),
                                     content='用户登录: %s' % request.user)
                if form.cleaned_data.get('rmb'):
                    request.session.set_expiry(60 * 60 * 24 * 7)
            else:
                result['message'] = '用户名或密码错误'

        else:
            if 'verify_code' in form.errors:
                result['message'] = '验证码错误或过期'
            else:
                result['message'] = '用户名或密码错误'
                print(form.errors['password'])
        return HttpResponse(json.dumps(result))

def logout_view(request):
    Audit.objects.create(type='用户退出',
                         user=request.user,
                         action='用户退出',
                         action_ip=login_ip(request),
                         content='用户退出 %s' % request.user)
    logout(request)
    return HttpResponseRedirect("/login/")

def register_view(request):
    if request.method == 'GET':
        return render(request,'register.html')
    elif request.method == 'POST' and request.is_ajax():
        result = {'status':False,'message':None}
        form = RegisterForm(request=request,data=request.POST)
        if form.is_valid() and request.is_ajax():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            username = form.cleaned_data.get('username')
            user_info = User_Profile.objects.filter(email=email).first()
            if not user_info:
                user = User_Profile.objects.create_user(email=email,password=password,name=username)
                # user.is_superuser = True
                user.is_active = True
                user.is_staff = True
                user.save()
                result['status'] = True
                Audit.objects.create(type='用户注册',
                                     user=email,
                                     action='注册',
                                     action_ip=login_ip(request),
                                     content='用户注册成功: %s' % request.user)
            else:
                result['message'] = '用户名已存在'
            return HttpResponse(json.dumps(result))
        else:
            print(form.errors)
            if '__all__' in form.errors:
                result['message'] = '两次密码输入不一致'
            elif 'password' in form.errors:
                result['message'] = '密码不能少于8位'
        return HttpResponse(json.dumps(result))

@login_required
def dashboard(request):
    asset_count = Asset.objects.all().count()
    asset_type = Asset.objects.all()
    physics_count = Asset.objects.filter(asset_type='physics').count()
    server_count = Asset.objects.filter(asset_type='server').count()
    database_count = Asset.objects.filter(asset_type='database').count()
    nosql_count = Asset.objects.filter(asset_type='nosql').count()
    inside_count = Asset.objects.filter(asset_type='inside').count()

    return render(request, 'index.html', {
        'asset_count': asset_count, 'asset_type': asset_type, 'physics_count': physics_count,
        'server_count': server_count, 'database_count': database_count, 'nosql_count': nosql_count,
        'inside_count': inside_count
    })


def user_list(request):
    all_user = User_Profile.objects.all()
    return render(request,'userperm/user-list.html',{'all_user':all_user})

# @permission_required('userperm.change_user',login_url='/noperm/')
def user_manage(request,uid=None,action=None):
    if uid:
        user = get_object_or_404(User_Profile, pk=uid)
        if action == 'edit':
            page_name = '编辑用户'
        if action == 'delete':
            user.delete()
            Audit.objects.create(type='用户管理',
                                   user=request.user.first_name,
                                   action='删除用户',
                                   action_ip=login_ip(request),
                                   content='删除用户 %s%s，用户名 %s' % (user.last_name, user.first_name, user.username))
            return redirect('user_list')
    else:
        user = User_Profile()
        action = 'add'
        page_name = '新增用户'

    if request.method == 'POST':
        print(request.POST)
        form = UserModelForm(request.POST,instance=user)
        print('===>%s' % form)
        if form.is_valid():
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            group_select = request.POST.getlist('group_sel')
            group_delete = request.POST.getlist('group_del')
            perm_select = request.POST.getlist('perm_sel')
            perm_delete = request.POST.getlist('perm_del')
            if action == 'add' or action == 'edit':
                form.save()
                if password1 and password1 == password2:
                    user.set_password(password1)
                user.save()
                user.group.add(*group_select)
                user.group.remove(*group_delete)
                user.user_permissions.add(*perm_select)
                user.user_permissions.remove(*perm_delete)
                Audit.objects.create(type='用户管理',
                                       user=request.user.first_name,
                                       action='编辑',
                                       action_ip=login_ip(request),
                                       content='%s %s%s，用户名 %s' % (
                                           '编辑', user.last_name, user.first_name, user.username))
                return redirect('user_list')
    else:
        form = UserModelForm(instance=user)
    return render(request,'userperm/user-manage.html',{'form': form,  'action': action, 'uid': uid})

def user_noperm(request):
    return render(request,'userperm/forbidden.html')

def audit_log(request):
    logs = Audit.objects.all()[:300]
    if request.method == 'GET':
        if request.GET.get('uid'):
            aid = request.get_full_path().split('=')[1]
            log_detail = Audit.objects.filter(id=aid)
            return render(request, 'userperm/audit-detail.html',
                          {'log_detail': log_detail})

    return render(request, 'userperm/audit.html', {'logs': logs})



def group_list(request):
    obj = Group.objects.all()
    return render(request,'userperm/group-list.html',{'obj':obj})