# coding: utf-8

from django.test import TestCase
from django.core.urlresolvers import reverse as r
from django.contrib.auth.models import User, Group


class IndexTest(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='vitor', email='vitor.freitas@oulu.fi', password='p4ssw0rd')
        user.is_superuser = True
        user.save()
        self.client.login(username='vitor', password='p4ssw0rd')
        self.resp = self.client.get(r('users:groups:index'))

    def test_get(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'groups/index.html')

