from django import forms
from django.contrib.auth.models import User

from value.deliverables.models import Deliverable
from value.users.forms import StakeholderMultipleModelChoiceField


class UploadFileForm(forms.Form):
    file = forms.FileField()


class DeliverableForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}), max_length=255)
    description = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control expanding', 'rows': '1'}), max_length=2000, required=False)
    stakeholders = StakeholderMultipleModelChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=User.objects.filter(is_active=True).order_by('first_name', 'last_name', 'username'), 
        required=False
        )

    class Meta:
        model = Deliverable
        fields = ['name', 'description', 'stakeholders']
