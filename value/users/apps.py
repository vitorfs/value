
# coding: utf-8

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UsersConfig(AppConfig):
    name = 'value.users'
    verbose_name = _('users')

    def ready(self):
        import value.users.signals.handlers  # noqa
