# -*- coding:utf-8 -*-  

from django import forms
from django.forms import fields
from django.core.exceptions import ValidationError
from .models import User_Profile

class BaseForm(object):
    def __init__(self,request,*args,**kwargs):
        self.request = request
        super(BaseForm,self).__init__(*args,**kwargs)

class LoginForm(BaseForm,forms.Form):
    username = fields.CharField(error_messages={'required':'邮箱不能为空'})
    password = fields.CharField(error_messages={'required':'密码不能为空'})
    rmb = fields.IntegerField(required=False)
    verify_code = fields.CharField(
        error_messages={'required':'验证码不能为空'}
    )
    def chean_verify_code(self):
        if self.request.session.get('verify_code').upper() != self.request.POST.get('verify_code').upper():
            raise ValidationError(message='验证码错误',code='invalid')

class RegisterForm(BaseForm,forms.Form):
    email = fields.EmailField()
    username = fields.CharField()
    password = fields.CharField(
        min_length=8,
        max_length=32,
        error_messages={'required': '密码不能为空.',
                        'invalid': '密码必须包含数字，字母、特殊字符',
                        'min_length': "密码长度不能小于8个字符",
                        'max_length': "密码长度不能大于32个字符"}
    )
    confirm_pwd = fields.CharField()

    def clean(self):
        value_dic = self.cleaned_data
        pwd = value_dic.get('password')
        pwd1 = value_dic.get('confirm_pwd')
        if pwd != pwd1:
            raise ValidationError("两次密码输入不一致")
        return self.cleaned_data

class UserModelForm(forms.ModelForm):
    class Meta:
        model = User_Profile
        fields = ('name', 'email','is_active','is_admin')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '姓名', 'required': 'required',
                                               'data-validate-length-range': '5,30'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': 'required'}),
            'is_active': forms.CheckboxInput(attrs={'style': 'padding-top:5px;'}),
            'is_admin': forms.CheckboxInput(attrs={'style': 'padding-top:5px;'}),
        }
