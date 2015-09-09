from django import forms
from django.contrib.auth.models import Group, User

from value.users.forms import StakeholderMultipleModelChoiceField


class GroupForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}), max_length=80)
    stakeholders = StakeholderMultipleModelChoiceField(queryset=User.objects.filter(is_active=True).order_by('first_name', 'last_name', 'username'), required=False)

    class Meta:
        model = Group
        fields = ['name', 'stakeholders',]

    def save(self, commit=True):
        instance = super(GroupForm, self).save(commit=False)   
        if commit:
            instance.save()
            instance.user_set.clear()
            instance.user_set.add(*self.cleaned_data['stakeholders'])
        return instance
