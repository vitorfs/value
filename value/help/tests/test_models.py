# coding: utf-8

from model_mommy import mommy

from django.test import TestCase

from value.help.models import Article


class HelpModelsTests(TestCase):

    def setUp(self):
        self.article = mommy.make(Article, name='How to create a deliverable')

    def test_help_article_unicode(self):
        self.assertTrue(isinstance(self.article, Article))
        self.assertEqual(self.article.__unicode__(), 'How to create a deliverable')
