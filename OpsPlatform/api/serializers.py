# -*- coding:utf-8 -*-  

from rest_framework import serializers

from django.contrib.auth.models import Group
from userperm.models import User_Profile

from assets.models import *

#用户
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Profile
        fields = ('id','email','password','is_active',
                  'is_admin','name','groups',
                  'tel','date_joined')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id','name')

#资产
class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = Asset
        fields = ('id','asset_type','name','loaction',
                  'management_ip','project','provider',
                  'status','server_info')
#主机
class AssetServerSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = Asset_Server
        fields = ('id','ip_addr','hostname','username',
                  'password','port','system_type',
                  'system_version','cpu','disk','memory')
























