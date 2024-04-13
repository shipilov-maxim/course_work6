import datetime

from django import template

register = template.Library()


@register.simple_tag
def current_time(format_string):
    dt_obj = datetime.datetime.now()
    return dt_obj.strftime(format_string)


@register.simple_tag
def media(data):
    if data:
        return f'/media/{data}'
    return '/media/none.jpg'


@register.filter
def string_slice(string: str):
    if len(string) > 200:
        return string[:200] + '...'
    return string
