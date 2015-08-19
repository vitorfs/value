# coding: utf-8

from django.test import TestCase
from django.core.urlresolvers import reverse as r
from django.contrib.auth.models import User

from value.factors.models import Factor, Group
from value.factors.forms import GroupForm
from value.measures.models import Measure


class EditGroupTest(TestCase):
    fixtures = ['development_auth_initial_data', 'development_measures_initial_data', 'development_factors_initial_data',]

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=1)
        cls.user.set_password('123')
        cls.user.save()
        cls.group = Group.objects.create(name='Maintainability')

    def setUp(self):
        self.client.login(username=self.user.username, password='123')
        self.response = self.client.get(r('factors:edit_group', args=(self.group.pk,)))

    def test_loaded_fixture(self):
        self.assertGreater(User.objects.all().count(), 0)
        self.assertGreater(Factor.objects.all().count(), 0)
        self.assertGreater(Measure.objects.all().count(), 0)

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_context(self):
        form = self.response.context['form']
        self.assertIsInstance(form, GroupForm)
