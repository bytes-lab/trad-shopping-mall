from django import template

register = template.Library()

@register.filter(name='value_in_dict')
def value_in_dict(value, arg):
    return value[int(arg)]

@register.filter(name='has_next_page')
def has_next_page(value, arg):
    return value[int(arg)].has_next()

@register.filter(name='has_prev_page')
def has_prev_page(value, arg):
    return value[int(arg)].has_previous()

@register.filter(name='cur_page')
def cur_page(value, arg):
    return value[int(arg)].number

@register.filter(name='value_in_list')
def value_in_list(value, arg):
    return value[int(arg)]

@register.filter(name='split')
def split(value, arg):
    return value.split(arg)

@register.filter(name='first_valid')
def first_valid(value):
    uploads = value.split(',')
    for idx in uploads:
        if idx != '0':
            return idx
