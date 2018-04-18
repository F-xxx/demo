from django.shortcuts import render,HttpResponse,get_object_or_404,HttpResponseRedirect
from .models import Asset,Asset_Server
from .forms import AssetModeForm,ServerModeForm
import xlwt
from io import StringIO
from utils.excel import SheetWrite
# Create your views here.

def asset_list(request):
    ass_list = Asset.objects.all()
    if request.GET.get('nid'):
        nid = request.get_full_path().split('=')
        server_detail = Asset.objects.filter(pk=nid).first()
        return render(request, 'asset/asset-detail.html', {'server_detail': server_detail})
    if request.GET.get('export'):
        pass
    return render(request, 'asset/asset-list.html', {'ass_list':ass_list})

def asset_manage(request,nid=None,action=None):
    if nid:
        server_obj = get_object_or_404(Asset_Server,pk=nid)
        asset_obj = Asset.objects.filter(server_info=server_obj).first()
        if action == 'delete':
            server_obj.delete()
            return HttpResponseRedirect('/asset/list')
        if request.method == 'POST':
            server_form = ServerModeForm(request.POST, instance=server_obj)
            asset_form = AssetModeForm(request.POST,instance=asset_obj)
            if all([asset_form.is_valid(),server_form.is_valid()]):
                if action == 'edit':
                    server_form.save()
                    asset_form.save()
                    return HttpResponseRedirect('/asset/list')
        else:
            asset_form = AssetModeForm(instance=asset_obj)
            server_form = ServerModeForm(instance=server_obj)
        return render(request,'asset/asset-manage.html',{'asset_form':asset_form,'server_form':server_form,'action':action})

def asset_add(request):

    if request.method == "POST":
        form = AssetModeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/asset/list')
    else:
        form = AssetModeForm()
    return render(request, 'asset/asset-add.html',{'form': form})

def server_add(request):

    if request.method == "POST":
        form = ServerModeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/asset/add')
    else:
        form = ServerModeForm()
    return render(request, 'asset/server-add.html',{'form': form})

def test_chart(request):
    asset_count = Asset.objects.all().count()
    asset_type = Asset.objects.all()
    physics_count = Asset.objects.filter(asset_type='physics').count()
    server_count = Asset.objects.filter(asset_type='server').count()
    database_count = Asset.objects.filter(asset_type='database').count()
    nosql_count = Asset.objects.filter(asset_type='nosql').count()
    inside_count = Asset.objects.filter(asset_type='inside').count()

    return render(request,'asset/chart.html',{
        'asset_count':asset_count,'asset_type':asset_type,'physics_count':physics_count,
        'server_count':server_count,'database_count':database_count,'nosql_count':nosql_count,
        'inside_count':inside_count
    })
