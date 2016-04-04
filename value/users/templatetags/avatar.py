# coding: utf-8

from django import template
from django.contrib.auth.models import User
from django.utils.html import mark_safe, escape

register = template.Library()


@register.simple_tag
def avatar(user, size=128, margin_right=0):
    avatar_template = u'''<span class="avatar"
                               alt="{display_name}"
                               data-toggle="tooltip"
                               data-placement="top"
                               data-container="body"
                               title="{display_name}"
                               style="background-color: {bg_color};
                                      width: {size}px;
                                      height: {size}px;
                                      font-size: {font_size}px;
                                      padding-top: {padding_top}px;
                                      margin-right: {margin_right}px">{initials}</span>'''
    font_size = size / 2
    padding_top = font_size / 4
    avatar_data = user.profile.get_avatar()
    format_kwargs = {
        'initials': escape(avatar_data[0]),
        'display_name': escape(user.profile.get_display_name()),
        'bg_color': avatar_data[1],
        'size': size,
        'font_size': font_size,
        'padding_top': padding_top,
        'margin_right': margin_right
    }
    return mark_safe(avatar_template.format(**format_kwargs))


@register.simple_tag
def avatar_id(pk, size=128, margin_right=0):
    user = User.objects.get(pk=pk)
    return avatar(user, size, margin_right)
