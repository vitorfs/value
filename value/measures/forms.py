# coding: utf-8

from django import forms

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
        label='Active',
        help_text='Unselect this instead of deleting measures.')
    
    class Meta:
        model = Measure
        fields = ('name', 'is_active',)
