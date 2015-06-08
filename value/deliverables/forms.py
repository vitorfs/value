from django import forms
from django.contrib.auth.models import User

from value.deliverables.models import Deliverable, Rationale


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


class UploadFileForm(forms.Form):
    file = forms.FileField()


class DeliverableForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}), max_length=255)
    description = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control expanding', 'rows': '1'}), max_length=2000, required=False)
    stakeholders = StakeholderPanelGroupMultipleModelChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=User.objects.filter(is_active=True).order_by('first_name', 'last_name', 'username'), 
        required=False
        )

    class Meta:
        model = Deliverable
        fields = ['name', 'description', 'stakeholders',]
        
class DeliverableBasicDataForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}), max_length=255)
    description = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control expanding', 'rows': '1'}), max_length=2000, required=False)

    class Meta:
        model = Deliverable
        fields = ['name', 'description',]
        
class RationaleForm(forms.ModelForm):
    class Meta:
        model = Rationale
        fields = ['text',]