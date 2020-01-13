from django.contrib.auth.forms import UserChangeForm
from django import forms

from onboard.models import Profile
TRUE_FALSE_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)


class SettingsForm(UserChangeForm):

    receive_email = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, widget=forms.Select())
    is_idle = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, widget=forms.Select())
    password = None

    class Meta:
        model = Profile
        fields= {
            'receive_email',
            'is_idle'
        }
