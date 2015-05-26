from django import forms

from value.deliverables.models import Deliverable


class UploadFileForm(forms.Form):
    file = forms.FileField()


class DeliverableForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}), max_length=255)
    description = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control expanding', 'rows': '1'}), max_length=2000, required=False)

    class Meta:
        model = Deliverable
        fields = ['name', 'description',]
