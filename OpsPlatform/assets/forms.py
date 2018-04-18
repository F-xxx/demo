# -*- coding:utf-8 -*-  

from .models import Asset,Asset_Server
from django import forms

class AssetModeForm(forms.ModelForm):
    class Meta:
        model = Asset
        # exclude = ['server_info']
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}, ),
            'loaction': forms.Select(attrs={'class': 'form-control'}),
            'management_ip': forms.TextInput(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
            'provider': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'asset_type': forms.Select(attrs={'class': 'form-control'}),
            'server_info': forms.Select(attrs={'class': 'form-control'}),
        }

class ServerModeForm(forms.ModelForm):
    class Meta:
        model = Asset_Server
        fields = '__all__'
        widgets = {
            'ip_addr': forms.TextInput(attrs={'class': 'form-control'}, ),
            'hostname': forms.TextInput(attrs={'class': 'form-control'}, ),
            'username': forms.TextInput(attrs={'class': 'form-control'}, ),
            'password': forms.TextInput(attrs={'class': 'form-control'}, ),
            'port': forms.NumberInput(attrs={'class': 'form-control'}, ),
            'system_type': forms.Select(attrs={'class': 'form-control'}),
            'system_version': forms.Select(attrs={'class': 'form-control'}),
            'cpu': forms.NumberInput(attrs={'class': 'form-control'}, ),
            'disk': forms.NumberInput(attrs={'class': 'form-control'}, ),
            'memory': forms.NumberInput(attrs={'class': 'form-control'}, ),
        }

