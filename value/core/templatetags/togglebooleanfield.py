# coding: utf-8

from django import template
from django.utils.html import escape

register = template.Library()


@register.simple_tag
def toggle_boolean(obj):
    icon = '<span class="glyphicon glyphicon-remove-sign text-danger"></span>'
    if obj.is_active:
        icon = '<span class="glyphicon glyphicon-ok-sign text-success"></span>'
    component = '<span class="js-toggle-active btn-active" data-id="{0}" data-is-active="{1}">{2}</span>'.format(obj.pk, obj.is_active, icon)
    return component
