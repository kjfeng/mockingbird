from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from multiselectfield import MultiSelectField

from onboard.models import Profile, YEAR_IN_SCHOOL_CHOICES, INDUSTRY_CHOICES

class MatchConfigurationForm(forms.Form):
    FILTER_CHOICES = [
        ('Industry', 'Industry'),
        ('Role', 'Role'),
        ('Year In School', 'Year In School'),
    ]

    filter_by = forms.MultipleChoiceField(required=False,
        choices=FILTER_CHOICES)

    class Meta():
        fields = ('filter_by',)

    
