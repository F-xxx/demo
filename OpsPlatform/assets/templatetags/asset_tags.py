# -*- coding:utf-8 -*-  

from django import template
from django.contrib.auth.models import Group,Permission
from django.db.models import Q
from ..models import Asset


register = template.Library()
def asset_count():
    pass

