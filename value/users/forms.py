# coding: utf-8

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class AccountForm(forms.ModelForm):
    first_name = forms.CharField(
        label=_('First name'),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=False
    )
    last_name = forms.CharField(
        label=_('Last name'),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=False
    )
    email = forms.EmailField(
        label=_('Email address'),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=254,
        required=False
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
