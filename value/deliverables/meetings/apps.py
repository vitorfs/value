# coding: utf-8

from django.apps import AppConfig


class MeetingsConfig(AppConfig):
    name = 'value.deliverables.meetings'
    verbose_name = 'Meetings'

    def ready(self):
        import value.deliverables.meetings.signals.handlers #noqa