#coding:utf8
from django import template
register = template.Library()

# 定义一个将日期中的月份转换为大写的过滤器，如8转换为八
@register.filter
def month_to_upper(value):
    return ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二'][value.month-1]