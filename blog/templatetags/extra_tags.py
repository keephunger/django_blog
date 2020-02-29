# my_filter.py
from django import template
register = template.Library()
@register.filter
def link_str(value):  # 定义过滤器
    value = str(value).split('<')[1]
    return value.strip('p>')