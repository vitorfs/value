# coding: utf-8

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse as r
from django.contrib.auth.models import User

from value.deliverables.models import Deliverable, DecisionItem
from value.deliverables.meetings.models import Meeting, MeetingItem, MeetingStakeholder
from value.factors.models import Factor
from value.measures.models import Measure


class FinalDecisionTestCase(TestCase):
    '''
    Final Decision View
    Base class with setup test data and fixtures
    '''
    fixtures = ['development_auth_initial_data', 'development_measures_initial_data', 'development_factors_initial_data',]

    @classmethod
    def setUpTestData(cls):
        user = User.objects.get(pk=1)
        user.set_password('123')
        user.save()

        User.objects.create_user(username='stakeholder_1', email='stakeholder_1@company.com', password='123')
        User.objects.create_user(username='stakeholder_2', email='stakeholder_2@company.com', password='123')

        deliverable = Deliverable.objects.create(name='Product 1', measure=Measure.get(), manager=user, created_by=user)
        deliverable.factors = Factor.list()
        deliverable.stakeholders = User.objects.all()
        DecisionItem.objects.create(deliverable=deliverable, name='Feature 1', created_by=user)
        DecisionItem.objects.create(deliverable=deliverable, name='Feature 2', created_by=user)
        DecisionItem.objects.create(deliverable=deliverable, name='Feature 3', created_by=user)

        meeting = Meeting.objects.create(name='Meeting 1', deliverable=deliverable, started_at=timezone.now(), created_by=user)

        for decision_item in deliverable.decisionitem_set.all():
            MeetingItem.objects.create(meeting=meeting, decision_item=decision_item)

        for stakeholder in deliverable.stakeholders.all():
            MeetingStakeholder.objects.create(meeting=meeting, stakeholder=stakeholder)

        cls.user = user
        cls.meeting = meeting

    def setUp(self):
        self.client.login(username=self.user.username, password='123')


class FinalDecisionTest(FinalDecisionTestCase):
    '''
    Basic view testing
    '''
    def setUp(self):
        super(FinalDecisionTest, self).setUp()
        self.response = self.client.get(r('deliverables:meetings:final_decision', args=(self.meeting.deliverable.pk, self.meeting.pk)))

    def test_loaded_fixture(self):
        self.assertGreater(User.objects.all().count(), 0)
        self.assertGreater(Factor.objects.all().count(), 0)
        self.assertGreater(Measure.objects.all().count(), 0)

    def test_get(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'meetings/final_decision.html')

    def test_context(self):
        meeting = self.response.context['meeting']
        formset = self.response.context['formset']
        self.assertIsInstance(meeting, Meeting)
        self.assertIsNotNone(formset)


class OngoingMeetingFinalDecisionTest(FinalDecisionTestCase):
    '''
    Specific testing for Final Decision View having meeting status as ONGOING
    '''
    def setUp(self):
        super(OngoingMeetingFinalDecisionTest, self).setUp()
        self.meeting.status = Meeting.ONGOING
        self.meeting.save()
        self.response = self.client.get(r('deliverables:meetings:final_decision', args=(self.meeting.deliverable.pk, self.meeting.pk)))

    def test_html(self):
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, 'type="checkbox"', self.meeting.meetingitem_set.count())
        #self.assertContains(self.response, 'type="text"', self.meeting.meetingitem_set.count())

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')


class ClosedMeetingFinalDecisionTest(FinalDecisionTestCase):
    '''
    Specific testing for Final Decision View having meeting status as CLOSED
    '''
    def setUp(self):
        super(ClosedMeetingFinalDecisionTest, self).setUp()
        self.meeting.status = Meeting.CLOSED
        self.meeting.save()
        self.response = self.client.get(r('deliverables:meetings:final_decision', args=(self.meeting.deliverable.pk, self.meeting.pk)))

    def test_html(self):
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, 'type="checkbox"', 0)
        self.assertContains(self.response, 'type="text"', 0)


class MeetingNotFoundFinalDecisionTest(FinalDecisionTestCase):
    '''
    Test 404 status for Final Decision View
    '''
    def setUp(self):
        super(MeetingNotFoundFinalDecisionTest, self).setUp()
        self.response = self.client.get(r('deliverables:meetings:final_decision', args=(0, 0)))

    def test_not_found(self):
        self.assertEqual(404, self.response.status_code)


class LoginRequiredFinalDecisionTest(FinalDecisionTestCase):
    '''
    Test if view has login required decorator
    '''
    def setUp(self):
        '''
        Override base class method to avoid login
        '''
        self.response = self.client.get(r('deliverables:meetings:final_decision', args=(self.meeting.deliverable.pk, self.meeting.pk)))

    def test_login_required(self):
        self.assertEqual(302, self.response.status_code)
        self.assertRedirects(self.response, '{0}?next={1}'.format(r('signin'), r('deliverables:meetings:final_decision', args=(self.meeting.deliverable.pk, self.meeting.pk))))
