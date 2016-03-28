# coding: utf-8

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MeetingsConfig(AppConfig):
    name = 'value.deliverables.meetings'
    verbose_name = _('meetings')

    def ready(self):
        import value.deliverables.meetings.signals.handlers  # noqa
