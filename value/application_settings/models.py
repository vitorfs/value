from django.db import models

class ApplicationSetting(models.Model):

    EXCEL_SHEET_INDEX = 'EXCEL_SHEET_INDEX'
    EXCEL_ENTRY_ORIENTATION = 'EXCEL_ENTRY_ORIENTATION'
    EXCEL_STARTING_ROW_COLUMN = 'EXCEL_STARTING_COLUMN'
    EXCEL_IMPORT_TEMPLATE = 'EXCEL_IMPORT_TEMPLATE'
    PLAIN_TEXT_SEPARATOR = 'PLAIN_TEXT_SEPARATOR'
    PLAIN_TEXT_STARTING_LINE = 'PLAIN_TEXT_STARTING_LINE'
    DECISION_ITEMS_DEFAULT_ORDERING = 'DECISION_ITEMS_DEFAULT_ORDERING'
    DECISION_ITEMS_COLUMNS_DISPLAY = 'DECISION_ITEMS_COLUMNS_DISPLAY'

    APPLICATION_SETTINGS = (
        (EXCEL_SHEET_INDEX, 'Excel sheet index'),
        (EXCEL_ENTRY_ORIENTATION, 'Excel entry orientation'),
        (EXCEL_STARTING_ROW_COLUMN, 'Excel starting row/column'),
        (EXCEL_IMPORT_TEMPLATE, 'Excel import template'),
        (PLAIN_TEXT_SEPARATOR, 'Plain text separator'),
        (PLAIN_TEXT_STARTING_LINE, 'Plain text starting line'),
        (DECISION_ITEMS_DEFAULT_ORDERING, 'Decision items default ordering'),
        (DECISION_ITEMS_COLUMNS_DISPLAY, 'Decision items columns display'),
        )

    name = models.CharField(max_length=255, primary_key=True, choices=APPLICATION_SETTINGS)
    value = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name
