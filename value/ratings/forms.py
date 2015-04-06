from django import forms
from value.ratings.models import Rating

class RatingForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}), max_length=255)

    class Meta:
        model = Rating
        fields = ['name',]
