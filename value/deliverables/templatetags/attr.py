# coding: utf-8

from django import template
from django.utils.html import escape, mark_safe

register = template.Library()


@register.filter('attr')
def attr(obj, attr_name):
    if attr_name == 'description':
        value = obj.description_as_html()
    else:
        value = getattr(obj, attr_name)
        if value is None:
            value = ''
        if value.startswith('http://') or value.startswith('https://'):
            value = mark_safe(u'<a href="{0}" target="_blank">{0}</a>'.format(escape(value)))
    return value


@register.filter('dictkey')
def dictkey(dictionary, key):
    if isinstance(dictionary, dict):
        if key in dictionary.keys():
            return dictionary[key]
    if key:
        return key
    return ''
