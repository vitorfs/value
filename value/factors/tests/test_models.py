# coding: utf-8

from model_mommy import mommy

from django.test import TestCase

from value.factors.models import Factor, Group


class FactorsModelsTests(TestCase):

    def setUp(self):
        self.factor = mommy.make(Factor, name='Customer Satisfaction')
        self.group = mommy.make(Group, name='Customers')

    def test_factors_factor_unicode(self):
        self.assertTrue(isinstance(self.factor, Factor))
        self.assertEqual(self.factor.__unicode__(), 'Customer Satisfaction')

    def test_factors_group_unicode(self):
        self.assertTrue(isinstance(self.group, Group))
        self.assertEqual(self.group.__unicode__(), 'Customers')
