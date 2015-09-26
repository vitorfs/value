import datetime

from django import forms
from django.contrib.auth.models import User

from value.factors.models import Factor, Group as FactorGroup
from value.deliverables.meetings.models import Meeting, MeetingItem, Scenario


class MeetingForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255)
    started_at = forms.DateTimeField(
        widget=forms.DateTimeInput(format='%d/%m/%Y %H:%M', attrs={ 'class': 'form-control' }), 
        label='Starting at', 
        input_formats=['%d/%m/%Y %H:%M',],
        initial=datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
        )
    description = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control expanding', 'rows': '1'}), max_length=2000, required=False)
    location = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}), max_length=50, required=False)

    class Meta:
        model = Meeting
        fields = ['name', 'started_at', 'location', 'description',]


class MeetingItemFinalDecisionForm(forms.ModelForm):
    meeting_decision = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class' : 'final-decision'}), required=False)
    meeting_ranking = forms.FloatField(widget=forms.TextInput(attrs={'class' : 'form-control input-sm'}), required=False)

    class Meta:
        model = MeetingItem
        fields = ['meeting_decision',]


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


class ScenarioBuilderForm(forms.Form):
    meeting = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=Meeting.objects.all(), required=True)
    category = forms.CharField(widget=forms.HiddenInput(), required=True)

    def __init__(self, *args, **kwargs):
        super(ScenarioBuilderForm, self).__init__(*args, **kwargs)
        items_range = self.initial['meeting'].meetingitem_set.count()
        self.fields['meeting_items_count'].choices = [(choice, choice) for choice in range(1, items_range+1)]
        self.fields['criteria'].queryset = self.initial['meeting'].deliverable.measure.measurevalue_set.all()


class FactorsScenarioBuilderForm(ScenarioBuilderForm):
    meeting_items_count = forms.ChoiceField(label='Select decision items', required=True)
    factors = forms.ModelChoiceField(label='And build the best scenario related to', queryset=Factor.list(), required=True, empty_label=None)    
    criteria = forms.ModelChoiceField(label='Based on', queryset=None, required=True, empty_label=None)
    
    class Meta:
        fields = ('meeting', 'category', 'meeting_items_count', 'factors', 'criteria')


class FactorsGroupsScenarioBuilderForm(ScenarioBuilderForm):
    meeting_items_count = forms.ChoiceField(label='Select decision items', required=True)
    factors_groups = forms.ModelChoiceField(label='And build the best scenario related to', queryset=FactorGroup.objects.all(), required=True, empty_label=None)
    criteria = forms.ModelChoiceField(label='Based on', queryset=None, required=True, empty_label=None)
    
    class Meta:
        fields = ('meeting', 'category', 'meeting_items_count', 'factors_groups', 'criteria')

