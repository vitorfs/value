from django.db import models

class ApplicationSetting(models.Model):

    EXCEL_SHEET_INDEX = 'EXCEL_SHEET_INDEX'
    EXCEL_STARTING_COLUMN = 'EXCEL_STARTING_COLUMN'
    EXCEL_STARTING_ROW = 'EXCEL_STARTING_COLUMN'
    PLAIN_TEXT_SEPARATOR = 'PLAIN_TEXT_SEPARATOR'
    PLAIN_TEXT_STARTING_LINE = 'PLAIN_TEXT_STARTING_LINE'
    DECISION_ITEMS_DEFAULT_ORDERING = 'DECISION_ITEMS_DEFAULT_ORDERING'
    DECISION_ITEMS_COLUMNS_DISPLAY = 'DECISION_ITEMS_COLUMNS_DISPLAY'

    APPLICATION_SETTINGS = (
        (EXCEL_SHEET_INDEX, 'Excel sheet index'),
        (EXCEL_STARTING_COLUMN, 'Excel starting column'),
        (EXCEL_STARTING_ROW, 'Excel starting column'),
        (PLAIN_TEXT_SEPARATOR, 'Plain text separator'),
        (PLAIN_TEXT_STARTING_LINE, 'Plain text starting line'),
        (DECISION_ITEMS_DEFAULT_ORDERING, 'Decision items default ordering'),
        (DECISION_ITEMS_COLUMNS_DISPLAY, 'Decision items columns display'),
        )

    name = models.CharField(max_length=255, primary_key=True, choices=APPLICATION_SETTINGS)
    value = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name
