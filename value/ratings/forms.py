from django import forms
from value.ratings.models import Rating, RatingValue

class RatingForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}), max_length=255)
    is_active = forms.BooleanField(
        widget=forms.CheckboxInput(), 
        label='Active',
        help_text='Unselect this instead of deleting ratings.',
        required=False)

    class Meta:
        model = Rating
        fields = ['name', 'is_active',]
