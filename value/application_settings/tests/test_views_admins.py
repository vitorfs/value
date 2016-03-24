# coding: utf-8

from model_mommy import mommy

from django.test import TestCase
from django.core.urlresolvers import reverse as r
from django.contrib.auth.models import User


class ApplicationSettingsViewsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='John', email='john@doe.com', password='123', is_superuser=True)
        self.users = mommy.make(User, is_superuser=False, _quantity=4)  # PKs 2, 3, 4, 5
        self.admins = mommy.make(User, is_superuser=True, _quantity=4)  # PKs 6, 7, 8, 9
        self.client.login(username='John', password='123')


class IndexTests(ApplicationSettingsViewsTestCase):

    def setUp(self):
        super(IndexTests, self).setUp()
        self.response = self.client.get(r('settings:index'))

    def test_get(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'application_settings/index.html')

    def test_context(self):
        admins = self.response.context['admins']
        users = self.response.context['users']
        self.assertIsNotNone(admins)
        self.assertIsNotNone(users)
        self.assertEqual(admins.count(), 5)
        self.assertEqual(users.count(), 4)

    def test_html(self):
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, 'type="checkbox"', 9)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')


class AdminsTests(ApplicationSettingsViewsTestCase):

    def setUp(self):
        super(AdminsTests, self).setUp()
        data = dict(grant_user=[2, 3], revoke_user=[6, 7, 8])
        self.response = self.client.post(r('settings:admins'), data)

    def test_post(self):
        self.assertEqual(302, self.response.status_code)

    def test_updated_superuser_status_true(self):
        self.assertTrue(User.objects.get(pk=2).is_superuser)
        self.assertTrue(User.objects.get(pk=3).is_superuser)

    def test_updated_superuser_status_false(self):
        self.assertFalse(User.objects.get(pk=6).is_superuser)
        self.assertFalse(User.objects.get(pk=7).is_superuser)
        self.assertFalse(User.objects.get(pk=8).is_superuser)


class AdminsSuccessMessageTests(ApplicationSettingsViewsTestCase):

    def setUp(self):
        super(AdminsSuccessMessageTests, self).setUp()
        data = dict(grant_user=[2, 3])
        self.response = self.client.post(r('settings:admins'), data, follow=True)

    def test_message(self):
        self.assertContains(self.response, 'Administrators settings saved successfully!')
