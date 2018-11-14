# coding: utf-8

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from jira.exceptions import JIRAError

from value.factors.models import Factor
from value.measures.models import Measure
from value.deliverables.models import Deliverable


class StakeholderPanelGroupMultipleModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        name = obj.profile.get_display_name()
        if obj.groups.exists():
            groups = ''
            for group in obj.groups.all():
                groups += u'{0}, '.format(group.name)
            groups = groups[:-2]
            name = u'{0} <small class="text-muted">({1})</small>'.format(name, groups)
        return name


class FactorModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        name = obj.name
        if obj.group:
            name = u'{0} <small class="text-muted">({1})</small>'.format(obj.name, obj.group.name)
        if not obj.is_active:
            name = u'<span class="text-danger">{0} <small><strong>inactive</strong></small></span>'.format(name)
        return name


class UploadFileForm(forms.Form):
    file = forms.FileField()


class DeliverableForm(forms.ModelForm):
    name = forms.CharField(
        label=_('Name'),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255
    )
    description = forms.CharField(
        label=_('Description'),
        widget=forms.Textarea(attrs={'class': 'form-control expanding', 'rows': '1'}),
        max_length=2000,
        required=False
    )
    stakeholders = StakeholderPanelGroupMultipleModelChoiceField(
        label=_('Stakeholders'),
        widget=forms.CheckboxSelectMultiple(),
        queryset=User.objects.none(),
        required=False
    )
    factors = FactorModelMultipleChoiceField(
        label=_('Select value factors to be used within the decision-making meetings'),
        widget=forms.CheckboxSelectMultiple(),
        queryset=Factor.objects.select_related('group').filter(is_active=True),
        required=True
    )
    measure = forms.ModelChoiceField(
        label=_('Select the measure to be used within the decision-making meetings'),
        queryset=Measure.objects.filter(is_active=True),
        required=True,
        empty_label=None
    )

    class Meta:
        model = Deliverable
        fields = ['name', 'description', 'stakeholders', 'factors', 'measure']


class DeliverableBasicDataForm(forms.ModelForm):
    name = forms.CharField(
        label=_('Name'),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255
    )
    description = forms.CharField(
        label=_('Description'),
        widget=forms.Textarea(attrs={'class': 'form-control expanding', 'rows': '1'}),
        max_length=2000,
        required=False
    )

    class Meta:
        model = Deliverable
        fields = ['name', 'description']


class DeliverableRemoveStakeholdersForm(forms.Form):
    clear_user_related_data = forms.BooleanField(
        widget=forms.HiddenInput(),
        required=False
    )
    stakeholders = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=User.objects.all(),
        required=True
    )


class DeliverableFactorsForm(forms.ModelForm):
    factors = FactorModelMultipleChoiceField(
        label=_('Select value factors to be used within the decision-making meetings'),
        widget=forms.CheckboxSelectMultiple(),
        queryset=Factor.objects.select_related('group').all(),
        required=True
    )

    class Meta:
        model = Deliverable
        fields = ['factors', ]


class DeliverableMeasureForm(forms.ModelForm):
    measure = forms.ModelChoiceField(
        label=_('Select the measure to be used within the decision-making meetings'),
        queryset=Measure.objects.all(),
        required=True,
        empty_label=None
    )

    class Meta:
        model = Deliverable
        fields = ['measure', ]


class DeliverableAdminsForm(forms.ModelForm):
    class Meta:
        model = Deliverable
        fields = ['admins', ]
        widgets = {
            'admins': forms.CheckboxSelectMultiple()
        }


class JiraSearchIssuesForm(forms.Form):
    query = forms.CharField(
        widget=forms.Textarea(attrs={'rows': '3'}),
        max_length=4000,
        label=_('JQL Query')
    )

    def __init__(self, *args, **kwargs):
        self.jira = kwargs.pop('jira', None)
        super(JiraSearchIssuesForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(JiraSearchIssuesForm, self).clean()
        query = cleaned_data.get('query', '')
        try:
            self.issues = self.jira.search_issues(query)
        except JIRAError, je:
            print je
            self.add_error('query', je.text)
        return cleaned_data
