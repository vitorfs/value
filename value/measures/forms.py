from django import forms
from value.measures.models import Measure, MeasureValue

class MeasureForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}), max_length=255)
    is_active = forms.BooleanField(
        widget=forms.CheckboxInput(), 
        label='Active',
        help_text='Unselect this instead of deleting measures.',
        required=False)

    class Meta:
        model = Measure
        fields = ['name', 'is_active',]
