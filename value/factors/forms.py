from django import forms
from value.factors.models import Factor
from value.ratings.models import Rating

class FactorForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}), max_length=255)
    description = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control'}), max_length=2000)
    rating = forms.ModelChoiceField(widget=forms.Select(attrs={'class' : 'form-control'}), queryset=Rating.objects.filter(is_active=True), empty_label=None)

    class Meta:
        model = Factor
        fields = ['name', 'description', 'rating', 'is_active',]
