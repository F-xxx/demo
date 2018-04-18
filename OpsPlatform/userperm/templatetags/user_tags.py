# -*- coding:utf-8 -*-  

from django import template
from django.contrib.auth.models import Group,Permission
from django.db.models import Q
from ..models import User_Profile


register = template.Library()
def show_perms(uid,perm_type):
    select_permissions_dict = {}
    perm = Permission.objects.filter(
        Q(content_type__app_label__exact='userperm')
    ).values('pk','name')

    permissions_dict = {i['pk']: i['name'] for i in perm}

    if uid and perm_type == 'user':
        user = User_Profile.objects.filter(pk=uid).first()
        select_permissions_dict = {i['pk']: i['name'] for i in user.user_permissions.values('pk', 'name')}

        select_permissions_group_dict = {i['pk']: '%s（继承组）' % i['name'] for g in user.groups.all() for i in
                                         g.permissions.values('pk', 'name')}
        select_permissions_dict = dict(select_permissions_dict, **select_permissions_group_dict)

    elif uid and perm_type == 'user_group':
        group = Group.objects.filter(pk=uid).first()
        select_permissions_dict = {i['pk']: i['name'] for i in group.permissions.values('pk', 'name')}

    for i in select_permissions_dict:
        if i in permissions_dict:
            del permissions_dict[i]

    return {'permissions_dict': permissions_dict, 'select_permissions_dict': select_permissions_dict}
register.inclusion_tag('userperm/tag_permissions.html')(show_perms)