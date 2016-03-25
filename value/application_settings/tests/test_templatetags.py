# coding: utf-8

from django.test import TestCase
from django.template import Context, Template

from value.deliverables.models import DecisionItemLookup
from value.application_settings.templatetags import customfields as cf


class CustomFieldsTests(TestCase):

    def setUp(self):
        DecisionItemLookup.objects.create(column_name='column_1', column_label='Name')
        DecisionItemLookup.objects.create(
            column_name='column_2',
            column_label='Effort',
            column_type=DecisionItemLookup.FLOAT,
            column_display=False
        )
        self.fields = DecisionItemLookup.get_custom_fields()
        self.column_types = DecisionItemLookup.COLUMN_TYPES

    def test_custom_field_attr(self):
        self.assertEqual(cf.custom_field_attr(self.fields, 1, 'label'), 'Name')

    def test_custom_field_attr_invalid_index(self):
        self.assertEqual(cf.custom_field_attr(self.fields, 99, 'label'), '')

    def test_custom_field_attr_tag(self):
        out = Template(
            '{% load customfields %}'
            '{% for column_index in custom_fields_range %}'
            '{% custom_field_attr custom_fields column_index "label" %},'
            '{% endfor %}'
        ).render(Context({
            'custom_fields': self.fields,
            'custom_fields_range': range(1, 3)
        }))
        self.assertEqual(out, 'Name,Effort,')

    def test_custom_field_display(self):
        self.assertEqual(cf.custom_field_display(self.fields, 1), 'checked')

    def test_custom_field_display_false(self):
        self.assertEqual(cf.custom_field_display(self.fields, 2), '')

    def test_custom_field_display_invalid_index(self):
        self.assertEqual(cf.custom_field_display(self.fields, 99), '')

    def test_custom_field_display_tag(self):
        out = Template(
            '{% load customfields %}'
            '<input type="checkbox" {% custom_field_display custom_fields column_index %}>'
        ).render(Context({
            'custom_fields': self.fields,
            'column_index': 1
        }))
        self.assertEqual(out, '<input type="checkbox" checked>')

    def test_custom_field_is_active(self):
        self.assertEqual(cf.custom_field_is_active(self.fields, 1), 'checked')

    def test_custom_field_is_active_false(self):
        self.assertEqual(cf.custom_field_is_active(self.fields, 99), '')

    def test_custom_field_selected(self):
        self.assertEqual(cf.custom_field_selected(self.fields, 1, (DecisionItemLookup.STRING, 'String')), 'selected')

    def test_custom_field_selected_invalid_index(self):
        self.assertEqual(cf.custom_field_selected(self.fields, 99, (DecisionItemLookup.STRING, 'String')), '')

    def test_custom_field_sort_icon(self):
        field = self.fields['column_1']
        self.assertEqual(cf.custom_field_sort_icon(field, 'asc'), '<span class="fa fa-sort-alpha-asc"></span>')

    def test_custom_field_sort_icon_numeric(self):
        field = self.fields['column_2']
        self.assertEqual(cf.custom_field_sort_icon(field, 'asc'), '<span class="fa fa-sort-numeric-asc"></span>')
