# coding: utf-8

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User)

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
