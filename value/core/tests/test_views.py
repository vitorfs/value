# coding: utf-8

from django.test import TestCase
from django.core.urlresolvers import reverse as r
from django.contrib.auth.models import User


class HomeTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='John', email='john@doe.com', password='123', is_superuser=True)
        self.client.login(username='John', password='123')
        self.response = self.client.get(r('home'))

    def test_get(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/home.html')
