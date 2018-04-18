# -*- coding:utf-8 -*-  


from django import template

register = template.Library()

@register.simple_tag
def error_form(arg):
    if arg:
        return arg[0][0]
    else:
        return ''
