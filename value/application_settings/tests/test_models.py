# coding: utf-8

try:
    import cPickle as pickle
except:
    import pickle

from django.test import TestCase

from value.application_settings.models import ApplicationSetting


class ApplicationSettingTests(TestCase):

    def setUp(self):
        ApplicationSetting.objects.create(
            name=ApplicationSetting.EXCEL_SHEET_INDEX,
            value='0'
        )
        ApplicationSetting.objects.create(
            name=ApplicationSetting.EXCEL_ENTRY_ORIENTATION,
            value='row'
        )
        ApplicationSetting.objects.create(
            name=ApplicationSetting.EXCEL_STARTING_ROW_COLUMN,
            value='0'
        )
        ApplicationSetting.objects.create(
            name=ApplicationSetting.EXCEL_IMPORT_TEMPLATE,
            value=pickle.dumps({'name': 'A', 'description': 'B'})
        )
        ApplicationSetting.objects.create(
            name=ApplicationSetting.PLAIN_TEXT_SEPARATOR,
            value=''
        )
        ApplicationSetting.objects.create(
            name=ApplicationSetting.PLAIN_TEXT_STARTING_LINE,
            value=''
        )
        ApplicationSetting.objects.create(
            name=ApplicationSetting.DECISION_ITEMS_DEFAULT_ORDERING,
            value=''
        )
        ApplicationSetting.objects.create(
            name=ApplicationSetting.DECISION_ITEMS_COLUMNS_DISPLAY,
            value='name,description'
        )

    def test_application_setting_unicode(self):
        setting = ApplicationSetting.objects.get(pk=ApplicationSetting.EXCEL_SHEET_INDEX)
        self.assertTrue(isinstance(setting, ApplicationSetting))
        self.assertEqual(setting.__unicode__(), 'EXCEL_SHEET_INDEX:0')

    def test_application_setting_get(self):
        s = ApplicationSetting.get()
        self.assertTrue(isinstance(s[ApplicationSetting.DECISION_ITEMS_COLUMNS_DISPLAY], list))
        self.assertTrue(isinstance(s[ApplicationSetting.EXCEL_IMPORT_TEMPLATE], dict))
        self.assertTrue(isinstance(s[ApplicationSetting.EXCEL_STARTING_ROW_COLUMN], int))
        self.assertTrue(isinstance(s[ApplicationSetting.EXCEL_SHEET_INDEX], int))

    def test_application_setting_get_invalid_import_template(self):
        setting = ApplicationSetting.objects.get(pk=ApplicationSetting.EXCEL_IMPORT_TEMPLATE)
        setting.value = 'invalid_input'
        setting.save()
        s = ApplicationSetting.get()
        self.assertEqual(s[ApplicationSetting.EXCEL_IMPORT_TEMPLATE], dict())

    def test_application_setting_get_invalid_excel_starting_row_column(self):
        setting = ApplicationSetting.objects.get(pk=ApplicationSetting.EXCEL_STARTING_ROW_COLUMN)
        setting.value = 'invalid_input'
        setting.save()
        s = ApplicationSetting.get()
        self.assertEqual(s[ApplicationSetting.EXCEL_STARTING_ROW_COLUMN], 0)

    def test_application_setting_get_invalid_excel_sheet_index(self):
        setting = ApplicationSetting.objects.get(pk=ApplicationSetting.EXCEL_SHEET_INDEX)
        setting.value = 'invalid_input'
        setting.save()
        s = ApplicationSetting.get()
        self.assertEqual(s[ApplicationSetting.EXCEL_SHEET_INDEX], 0)

    def test_application_setting_get_empty_decision_items_column_display(self):
        setting = ApplicationSetting.objects.get(pk=ApplicationSetting.DECISION_ITEMS_COLUMNS_DISPLAY)
        setting.value = 'name,description,'
        setting.save()
        s = ApplicationSetting.get()
        self.assertEqual(s[ApplicationSetting.DECISION_ITEMS_COLUMNS_DISPLAY], ['name', 'description'])

    def test_application_setting_get_invalid_decision_items_column_display(self):
        setting = ApplicationSetting.objects.get(pk=ApplicationSetting.DECISION_ITEMS_COLUMNS_DISPLAY)
        setting.value = None
        setting.save()
        s = ApplicationSetting.get()
        self.assertEqual(s[ApplicationSetting.DECISION_ITEMS_COLUMNS_DISPLAY], ['name', 'description'])
