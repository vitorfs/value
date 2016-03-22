# coding: utf-8

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.html import escape

from value.factors.models import Factor, Group as FactorGroup
from value.measures.models import MeasureValue
from value.deliverables.models import Deliverable
from value.deliverables.meetings.models import Meeting, MeetingItem, Scenario, Rationale


class AbstractMeetingForm(forms.ModelForm):
    deliverable = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=Deliverable.objects.all(), required=True)
    name = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255)
    started_at = forms.DateTimeField(
        widget=forms.DateTimeInput(format='%d/%m/%Y %H:%M', attrs={ 'class': 'form-control' }), 
        label='Starting at', 
        input_formats=['%d/%m/%Y %H:%M',]
        )
    description = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control expanding', 'rows': '1'}), max_length=2000, required=False)
    location = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}), max_length=50, required=False)

class NewMeetingForm(AbstractMeetingForm):
    default_evaluation = forms.ModelChoiceField(
        widget=forms.Select(attrs={ 'class': 'form-control' }),
        queryset=MeasureValue.objects.none(), 
        required=False
        )

    class Meta:
        model = Meeting
        fields = ['deliverable', 'name', 'started_at', 'location', 'description', 'default_evaluation',]

    def __init__(self, *args, **kwargs):
        super(NewMeetingForm, self).__init__(*args, **kwargs)
        self.fields['default_evaluation'].queryset = self.instance.deliverable.measure.measurevalue_set.all()

class MeetingForm(AbstractMeetingForm):
    class Meta:
        model = Meeting
        fields = ['deliverable', 'name', 'started_at', 'location', 'description',]

class MeetingStatusForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['status']

class MeetingItemFinalDecisionForm(forms.ModelForm):
    meeting_decision = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class' : 'final-decision'}), required=False)
    meeting_ranking = forms.FloatField(widget=forms.TextInput(attrs={'class' : 'form-control input-sm'}), required=False)

    class Meta:
        model = MeetingItem
        fields = ['meeting_decision', 'meeting_ranking']


class ScenarioForm(forms.ModelForm):
    meeting = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=Meeting.objects.all(), required=True)
    meeting_items = forms.ModelMultipleChoiceField(
            widget=forms.CheckboxSelectMultiple(), 
            queryset=None,
            required=True
            )

    def __init__(self, *args, **kwargs):
        super(ScenarioForm, self).__init__(*args, **kwargs)
        self.fields['meeting_items'].queryset = self.instance.meeting.meetingitem_set.all()

    class Meta:
        model = Scenario
        fields = ('name', 'meeting', 'meeting_items')


class FactorMultipleModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        if obj.group:
            return u'<strong>{0}</strong>: {1}'.format(escape(obj.group.name), escape(obj.name))
        return escape(obj.name)

class ScenarioBuilderForm(forms.Form):
    name = forms.CharField(label='Name', max_length=255, required=True)
    meeting = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=Meeting.objects.all(), required=True)
    meeting_items_count = forms.ChoiceField(label='Number of decision items to compose the scenario', required=True)
    factors = FactorMultipleModelChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        label='Related to', 
        queryset=Factor.objects.none(), 
        required=True
        )
    criteria = forms.ModelChoiceField(label='Based on', queryset=None, required=True, empty_label=None)

    def __init__(self, *args, **kwargs):
        super(ScenarioBuilderForm, self).__init__(*args, **kwargs)
        items_range = self.initial['meeting'].meetingitem_set.count()
        self.fields['meeting_items_count'].choices = [(choice, choice) for choice in range(1, items_range+1)]
        self.fields['criteria'].queryset = self.initial['meeting'].measure.measurevalue_set.all()
        self.fields['factors'].queryset = self.initial['meeting'].factors.all()

    class Meta:
        fields = ('meeting', 'meeting_items_count', 'factors', 'criteria')

def validate_scenarios_selection(value):
    if len(value) != 2:
        raise ValidationError('Select exactly two scenarios to compare.')


class CompareScenarioForm(forms.Form):
    meeting = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=Meeting.objects.all(), required=True)
    scenarios = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(), 
        label='Select two scenarios to compare',
        queryset=Scenario.objects.none(), 
        required=True
        )

    def __init__(self, *args, **kwargs):
        super(CompareScenarioForm, self).__init__(*args, **kwargs)
        self.fields['scenarios'].queryset = self.initial['meeting'].scenarios.all()
        self.fields['scenarios'].validators.append(validate_scenarios_selection)

    class Meta:
        fields = ('meeting', 'meeting_items')


class RationaleForm(forms.ModelForm):
    class Meta:
        model = Rationale
        fields = ['text',]
