# coding: utf-8

from model_mommy import mommy

from django.test import TransactionTestCase

from value.measures.models import Measure, MeasureValue
from value.factors.models import Factor
from value.deliverables.models import Deliverable
from value.deliverables.meetings.forms import NewMeetingForm, ScenarioForm, ScenarioBuilderForm
from value.deliverables.meetings.models import Meeting, MeetingItem, Scenario


class NewMeetingFormTests(TransactionTestCase):

    def setUp(self):
        measure = mommy.make(Measure)
        values = mommy.make(MeasureValue, measure=measure, _quantity=3)
        self.values = map(repr, values)
        self.deliverable = mommy.make(Deliverable, measure=measure)

    def test_new_meeting_form_init(self):
        meeting = Meeting(deliverable=self.deliverable)
        form = NewMeetingForm(instance=meeting)
        form_queryset = form.fields['default_evaluation'].queryset
        self.assertQuerysetEqual(form_queryset, self.values, ordered=False)


class ScenarioFormTests(TransactionTestCase):

    def setUp(self):
        meeting = mommy.make(Meeting)
        self.scenario = Scenario(meeting=meeting)
        items = mommy.make(MeetingItem, meeting=meeting, _quantity=10)
        self.items = map(repr, items)

    def test_scenario_form_init(self):
        form = ScenarioForm(instance=self.scenario)
        meeting_items_queryset = form.fields['meeting_items'].queryset
        self.assertQuerysetEqual(meeting_items_queryset, self.items, ordered=False)


class ScenarioBuilderFormTests(TransactionTestCase):

    def setUp(self):
        measure = mommy.make(Measure)
        mommy.make(MeasureValue, measure=measure, _quantity=3)

        mommy.make(Factor, measure=measure, _quantity=10)

        self.meeting = mommy.make(Meeting, measure=measure)
        self.meeting.factors = Factor.objects.all()
        mommy.make(MeetingItem, meeting=self.meeting, _quantity=5)

        self.factors = map(repr, self.meeting.factors.all())
        self.criteria = map(repr, self.meeting.measure.measurevalue_set.all())

    def test_scenario_builder_form_init(self):
        form = ScenarioBuilderForm(initial={ 'meeting': self.meeting })

        choices = form.fields['meeting_items_count'].choices
        criteria_queryset = form.fields['criteria'].queryset
        factors_queryset = form.fields['factors'].queryset

        self.assertQuerysetEqual(criteria_queryset, self.criteria, ordered=False)
        self.assertQuerysetEqual(factors_queryset, self.factors, ordered=False)
        self.assertEqual(choices, [(1,1),(2,2),(3,3),(4,4),(5,5)])
