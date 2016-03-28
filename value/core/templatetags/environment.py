# coding: utf-8

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def environment():
    return settings.ENVIRONMENT_NAME
