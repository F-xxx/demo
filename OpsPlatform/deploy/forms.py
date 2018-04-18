# -*- coding:utf-8 -*-  

from django import forms
from .models import GameInfo

class UploadForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


file_path = forms.CharField(
        required=True,
        label=u"上传文件",
        widget=forms.TextInput(
            attrs={
                'rows': 2,
                'class': 'uk-width-1-2',
            }
        ),
    )


class GameInfoForm(forms.ModelForm):
    class Meta:
        model = GameInfo
        fields = '__all__'
        widgets = {
            'platform': forms.Select(attrs={'class': 'form-control'}, ),
            'operate': forms.Select(attrs={'class': 'form-control'}, ),
            'zone': forms.Select(attrs={'class': 'form-control'}, ),
        }
