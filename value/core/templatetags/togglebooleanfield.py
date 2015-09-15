# coding: utf-8

from django import template
from django.utils.html import escape

register = template.Library()


@register.simple_tag
def toggle_boolean(value):
    html = '<span class="glyphicon glyphicon-remove-sign text-danger"></span>'
    if value:
        html = '<span class="glyphicon glyphicon-ok-sign text-success"></span>'
    return html 
