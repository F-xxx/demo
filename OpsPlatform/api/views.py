from rest_framework import status
from .serializers import *
from assets.models import Asset,Asset_Server
from userperm.models import User_Profile
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required


# Create your views here.


@api_view(['GET','POST'])
@permission_required('asset.add_user',raise_exception=True)
def user_list(request,format=None):
    if request.method == 'GET':
        queryset = User_Profile.objects.all()
        serializer = UserSerializer(queryset,many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST','DELETE'])
@permission_required('asset.change_user',raise_exception=True)
def user_detail(request,pk,format=None):
    try:
        queryset = User_Profile.objects.get(pk=pk)
    except User_Profile.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = UserSerializer(queryset)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(queryset,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)

    elif request.method == 'DELETE':
        if not request.user.has_perm('assets.delete_user'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET','POST'])
@permission_required('asset.can_add_asset',raise_exception=True)
def asset_list(request,format=None):
    if request.method == 'GET':
        queryset = Asset.objects.all()
        serializer = AssetSerializer(queryset,many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AssetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST','DELETE'])
@permission_required('asset.can_change_asset',raise_exception=True)
def asset_detail(request,pk,format=None):
    try:
        queryset = Asset.objects.get(pk=pk)
    except Asset.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = AssetSerializer(queryset)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AssetSerializer(queryset,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)
    elif request.method == 'DELETE':
        if not request.user.has_perm('assets.can_delete_asset'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
@permission_required('asset.can_add_server',raise_exception=True)
def server_list(request,format=None):
    if request.method == 'GET':
        queryset = Asset_Server.objects.all()
        serializer = AssetServerSerializer(queryset,many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if request.data.get('data'):
            data = request.data.get('data')
        else:
            data = request.data
        serializer = AssetServerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST','DELETE'])
@permission_required('asset.can_change_server',raise_exception=True)
def server_detail(request,pk,format=None):
    try:
        queryset = Asset_Server.objects.get(pk=pk)
    except Asset_Server.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = AssetSerializer(queryset)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if request.data.get('data'):
            data = request.data.get('data')
        else:
            data = request.data
        serializer = AssetSerializer(queryset,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)
    elif request.method == 'DELETE':
        if not request.user.has_perm('assets.can_delete_server'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        queryset.delete()
        try:
            asset_queryset = Asset.objects.get(id=queryset.asset.pk)
        except Asset.DoesNotExist:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)



