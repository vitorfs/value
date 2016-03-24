# coding: utf-8

try:
    import cPickle as pickle
except:  # pragma: no cover
    import pickle

from django.db import models
from django.utils.translation import ugettext_lazy as _


class ApplicationSetting(models.Model):

    EXCEL_SHEET_INDEX = 'EXCEL_SHEET_INDEX'
    EXCEL_ENTRY_ORIENTATION = 'EXCEL_ENTRY_ORIENTATION'
    EXCEL_STARTING_ROW_COLUMN = 'EXCEL_STARTING_ROW_COLUMN'
    EXCEL_IMPORT_TEMPLATE = 'EXCEL_IMPORT_TEMPLATE'
    PLAIN_TEXT_SEPARATOR = 'PLAIN_TEXT_SEPARATOR'
    PLAIN_TEXT_STARTING_LINE = 'PLAIN_TEXT_STARTING_LINE'
    DECISION_ITEMS_DEFAULT_ORDERING = 'DECISION_ITEMS_DEFAULT_ORDERING'
    DECISION_ITEMS_COLUMNS_DISPLAY = 'DECISION_ITEMS_COLUMNS_DISPLAY'

    APPLICATION_SETTINGS = (
        (EXCEL_SHEET_INDEX, _('Excel sheet index')),
        (EXCEL_ENTRY_ORIENTATION, _('Excel entry orientation')),
        (EXCEL_STARTING_ROW_COLUMN, _('Excel starting row/column')),
        (EXCEL_IMPORT_TEMPLATE, _('Excel import template')),
        (PLAIN_TEXT_SEPARATOR, _('Plain text separator')),
        (PLAIN_TEXT_STARTING_LINE, _('Plain text starting line')),
        (DECISION_ITEMS_DEFAULT_ORDERING, _('Decision items default ordering')),
        (DECISION_ITEMS_COLUMNS_DISPLAY, _('Decision items columns display')),
        )

    name = models.CharField(_('name'), max_length=255, primary_key=True, choices=APPLICATION_SETTINGS)
    value = models.CharField(_('value'), max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'application_settings'

    def __unicode__(self):
        return '{0}:{1}'.format(self.name, self.value)

    @staticmethod
    def get():
        settings = {}

        for k, v in ApplicationSetting.APPLICATION_SETTINGS:
            if k == ApplicationSetting.DECISION_ITEMS_COLUMNS_DISPLAY:
                settings[k] = ['name', 'description']
            else:
                settings[k] = ''

        for setting in ApplicationSetting.objects.all():

            if setting.name == ApplicationSetting.EXCEL_IMPORT_TEMPLATE:
                try:
                    settings[setting.name] = pickle.loads(str(setting.value))
                except:
                    settings[setting.name] = {}

            elif setting.name == ApplicationSetting.EXCEL_STARTING_ROW_COLUMN or \
                    setting.name == ApplicationSetting.EXCEL_SHEET_INDEX:
                try:
                    settings[setting.name] = int(setting.value)
                except:
                    settings[setting.name] = 0

            elif setting.name == ApplicationSetting.DECISION_ITEMS_COLUMNS_DISPLAY:
                try:
                    settings[setting.name] = setting.value.split(',')
                    if settings[setting.name]:
                        if not len(settings[setting.name][-1]):
                            del settings[setting.name][-1]
                except:
                    settings[k] = ['name', 'description']

            else:
                settings[setting.name] = setting.value
        return settings
