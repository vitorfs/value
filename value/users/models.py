# coding: utf-8

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify


class Profile(models.Model):
    user = models.OneToOneField(User)
    is_external = models.BooleanField(default=False)

    class Meta:
        db_table = 'auth_user_profile'
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __unicode__(self):
        return self.get_display_name()

    def get_display_name(self):
        if self.user.first_name and self.user.last_name:
            return self.user.get_full_name()
        elif self.user.first_name:
            return self.user.first_name
        elif self.user.last_name:
            return self.user.last_name
        else:
            return self.user.username

    def get_display_roles(self):
        groups = self.user.groups.all().values_list('name', flat=True)
        return ', '.join(groups)

    def get_avatar(self):
        initials = u''

        if self.user.first_name and self.user.last_name:
            initials = u'{0}{1}'.format(self.user.first_name[:1], self.user.last_name[:1])
        elif self.user.first_name and len(self.user.first_name) > 1:
            initials = self.user.first_name[:2]
        elif self.user.last_name and len(self.user.last_name) > 1:
            initials = self.user.last_name[:2]
        elif len(self.user.username) > 1:
            initials = self.user.username[:2]
        else:
            initials = self.user.username

        initials = slugify(initials)

        colors = {
            'a': '#8A2E60',
            'b': '#4B2D73',
            'c': '#AA5A39',
            'd': '#29516D',
            'e': '#6F256F',
            'f': '#993350',
            'g': '#2D882D',
            'h': '#AA8E39',
            'i': '#7F2A68',
            'j': '#403075',
            'k': '#AA5439',
            'l': '#7B9F35',
            'm': '#AA7939',
            'n': '#AA8539',
            'o': '#AAA839',
            'p': '#236467',
            'q': '#AA9739',
            'r': '#592A71',
            's': '#609732',
            't': '#277553',
            'u': '#AA9F39',
            'v': '#91A437',
            'w': '#343477',
            'x': '#2E4372',
            'y': '#AA6D39',
            'z': '#AA3C39'
        }

        try:
            color = colors[initials[:1].lower()]
        except KeyError:
            color = '#E1E1E1'

        return (initials.upper(), color)
