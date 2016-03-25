# coding: utf-8

from django import forms
from django.utils.translation import ugettext_lazy as _

from value.measures.models import Measure


class BaseMeasureForm(forms.ModelForm):
    class Meta:
        model = Measure
        fields = ('name',)


class CreateMeasureForm(BaseMeasureForm):
    pass


class ChangeMeasureForm(BaseMeasureForm):
    is_active = forms.BooleanField(
        widget=forms.CheckboxInput(),
        label=_('Active'),
        help_text=_('Unselect this instead of deleting measures.'),
        required=False)

    class Meta:
        model = Measure
        fields = ('name', 'is_active',)
