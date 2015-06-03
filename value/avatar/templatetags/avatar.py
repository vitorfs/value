# -*- coding: utf-8 -*-

import os
import urllib

from django import template
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag
def avatar(user, size=128):

    initials = ''

    if user.first_name and user.last_name:
        initials = '{0}{1}'.format(user.first_name[:1], user.last_name[:1])
    elif user.first_name and len(user.first_name) > 1:
        initials = user.first_name[:2]
    elif user.last_name and len(user.last_name) > 1:
        initials = user.last_name[:2]
    elif len(user.username) > 1:
        initials = user.username[:2]
    else:
        initials = user.username

    colors =  { 
        'a': '8A2E60',
        'b': '4B2D73',
        'c': 'AA5A39',
        'd': '29516D',
        'e': '6F256F',
        'f': '993350',
        'g': '2D882D',
        'h': 'AA8E39',
        'i': '7F2A68',
        'j': '403075',
        'k': 'AA5439',
        'l': '7B9F35',
        'm': 'AA7939',
        'n': 'AA8539',
        'o': 'AAA839',
        'p': '236467',
        'q': 'AA9739',
        'r': '592A71',
        's': '609732',
        't': '277553',
        'u': 'AA9F39',
        'v': '91A437',
        'w': '343477',
        'x': '2E4372',
        'y': 'AA6D39',
        'z': 'AA3C39'
    }

    avatar_path = '{0}/avatar/{1}/{2}.png'.format(settings.MEDIA_ROOT, size, initials)

    if os.path.isfile(avatar_path):
        return '{0}avatar/{1}/{2}.png'.format(settings.MEDIA_URL, size, initials)
    else:
        url = '{0}?{1}'.format(
          reverse('avatar', args=(initials,)),
          urllib.urlencode({ 'size' : size, 'bg' : colors[initials[:1].lower()], 'fg' : 'ffffff' })
          )
        return url

@register.simple_tag
def avatar_id(pk, size=128):
    user = User.objects.get(pk=pk)
    return avatar(user, size)
    
@register.simple_tag
def avatar_img(user, size=128):
    src = avatar(user, size)
    return u'<img src="{0}" alt="{1}" class="img-circle" data-toggle="tooltip" data-placement="top" title="{1}">'.format(src, user.profile.get_display_name())
