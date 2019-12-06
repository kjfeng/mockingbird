from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

from onboard.models import Profile, YEAR_IN_SCHOOL_CHOICES, INDUSTRY_CHOICES


class EditAccountForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = {
            'email',
            'first_name'
        }

class EditProfileForm(UserChangeForm):
    year_in_school = forms.ChoiceField(choices=YEAR_IN_SCHOOL_CHOICES)

    industry = forms.MultipleChoiceField(choices=INDUSTRY_CHOICES)

    major = forms.CharField(required=False, widget=forms.Textarea(
        attrs={"rows":1, "cols":50}))

    role = forms.CharField(required=False, widget=forms.Textarea(
        attrs={"rows":1,"cols":50}))

    password = None

    class Meta:
        model = Profile
        fields = {
            'year_in_school',
            'major',
            'industry',
            'role',
        }
