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

    colors = { 'a' : 'AA3C39', 'b' : '993350', 'c' : '8A2E60', 'd' : '6F256F', 'e' : '592A71', 'f' : '4B2D73', 'g' : '403075', 'h' : '343477', 'i' : '2E4372', 'j' : '29516D', 'k' : '236467', 'l' : '277553', 'm' : '2D882D', 'n' : '609732', 'o' : '7B9F35', 'p' : '91A437', 'q' : 'AAA839', 'r' : 'AA9F39', 's' : 'AA9739', 't' : 'AA8E39', 'u' : 'AA8539', 'v' : 'AA7939', 'w' : 'AA6D39', 'x' : 'AA5A39', 'y' : 'AA5439', 'z' : '7F2A68' }

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
    