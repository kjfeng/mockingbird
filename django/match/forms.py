from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from multiselectfield import MultiSelectField

from onboard.models import Profile, RANK_CHOICES, INDUSTRY_MATCH_CHOICE

class MatchConfigurationForm(UserChangeForm):
    password = None
    industry_match = forms.ChoiceField(choices=INDUSTRY_MATCH_CHOICE)
    rank_by = forms.MultipleChoiceField(required=False,
        choices=RANK_CHOICES)

    class Meta():
        model = Profile
        fields = {
            'industry_match',
            'rank_by',
        }

    
