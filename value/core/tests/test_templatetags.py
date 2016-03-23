# coding: utf-8

from django.test import TestCase
from django.template import Context, Template

from value.core.templatetags import templatehelpers


class CoreTemplateTagsTemplateHelpersTests(TestCase):

    def setUp(self):
        pass

    def test_startswith(self):
        self.assertTrue(templatehelpers.startswith('/factors/add/', '/factors/'))

    def test_startswith_invalid_input(self):
        self.assertFalse(templatehelpers.startswith(dict(), '/factors/'))

    def test_startswith_tag(self):
        out = Template(
            '{% load templatehelpers %}'
            '<li{% if "/factors/add/"|startswith:"/factors/" %} class="active"{% endif %}>'
        ).render(Context())
        self.assertEqual(out, '<li class="active">')
