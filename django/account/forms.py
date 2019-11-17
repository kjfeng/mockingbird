from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

from onboard.models import Profile


class EditAccountForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = {
            'email',
        }

class EditProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = Profile
        fields = {
            'year_in_school',
            'major',
            'industry',
            'role',
        }