from django.contrib.auth.forms import UserChangeForm
from django import forms

from onboard.models import Profile


class SettingsForm(UserChangeForm):

    receive_email = forms.BooleanField(required=False)
    is_idle = forms.BooleanField(required=False)
    password = None

    class Meta:
        model = Profile
        fields= {
            'receive_email',
            'is_idle'
        }
