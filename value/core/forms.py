from django import forms
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string


class SurveyUserForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput, required=True, label='Email address')

    class Meta:
        fields = ('email',)

    def save(self):
        user = User.objects.create_user(
            username=get_random_string(10),
            password=None,
            email=self.cleaned_data.get('email')
        )
        user.refresh_from_db()
        user.profile.is_external = True
        user.save()
        return user
