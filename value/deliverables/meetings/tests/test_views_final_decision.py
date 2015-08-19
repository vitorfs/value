# coding: utf-8

from django.test import TestCase
from django.core.urlresolvers import reverse as r
from django.contrib.auth.models import User

from value.factors.models import Factor
from value.measures.models import Measure


class FinalDecisionTest(TestCase):

    fixtures = ['development_data',]

    def setUp(self):
        user = User.objects.get(username='vitor')
        user.set_password('123')
        user.save()
        
        self.client.login(username='vitor', password='123')
        self.response = self.client.get(r('home'))

    def test_loaded_fixture(self):
        self.assertGreater(User.objects.all().count(), 0)
        self.assertGreater(Factor.objects.all().count(), 0)
        self.assertGreater(Measure.objects.all().count(), 0)

    def test_get(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/home.html')
