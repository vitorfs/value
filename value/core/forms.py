from django import forms
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string


class SurveyUserForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput, required=True, label='Email address')

    class Meta:
        fields = ('email',)

    def save(self):
        email = self.cleaned_data.get('email')
        try:
            username = email.split('@')[0]
            if User.objects.filter(username=username).exists():
                username = '{}_{}'.format(username, get_random_string(5))
        except Exception, e:
            username = get_random_string(10)

        user = User.objects.create_user(
            username=username,
            password=None,
            email=email
        )
        user.refresh_from_db()
        user.profile.is_external = True
        user.save()
        return user
