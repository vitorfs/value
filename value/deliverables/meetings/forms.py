import datetime

from django import forms
from django.contrib.auth.models import User

from value.deliverables.meetings.models import Meeting


class MeetingForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255)
    started_at = forms.DateTimeField(
        widget=forms.TextInput(attrs={ 'class': 'form-control' }), 
        label='Starting at', 
        input_formats=['%d/%m/%Y %H:%M',],
        initial=datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
        )
    description = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control expanding', 'rows': '1'}), max_length=2000, required=False)
    location = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}), max_length=50, required=False)

    class Meta:
        model = Meeting
        fields = ['name', 'started_at', 'location', 'description',]
