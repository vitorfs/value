# coding: utf-8

from django import template

register = template.Library()

@register.filter('attr')
def attr(obj, attr_name):
    value = getattr(obj, attr_name)
    if value == None:
        value = ''
    return value

@register.filter('dictkey')
def dictkey(dictionary, key):
    if isinstance(dictionary, dict):
        if key in dictionary.keys():
            return dictionary[key]
    if key:
        return key
    return ''
