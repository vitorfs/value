from django import forms
from django.utils.translation import ugettext_lazy as _


class JIRAForm(forms.Form):
    enabled = forms.BooleanField(
        label=_(u'Enable JIRA integration'),
        required=False
    )
    value_ranking = forms.CharField(
        label=_(u'Value Ranking JIRA Custom Field ID'),
        max_length=255,
        required=False
    )
    value_ranking_summary = forms.CharField(
        label=_(u'Value Summary JIRA Custom Field ID'),
        max_length=255,
        required=False
    )

    class Meta:
        fields = ('value_ranking', 'value_ranking_summary',)
