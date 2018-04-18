# -*- coding:utf-8 -*-


from django import template
from django.contrib.auth.models import Group,Permission
from django.db.models import Q

from ..models import User_Profile

register = template.Library()


@register.filter(name='is_super')
def is_super_user(pk):
    if pk:
        return User_Profile.objects.filter(pk=pk).first().is_superuser
    else:
        return None






















