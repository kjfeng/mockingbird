from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from multiselectfield import MultiSelectField

from onboard.models import Profile, RANK_CHOICES, INDUSTRY_MATCH_CHOICE

class MatchConfigurationForm(UserChangeForm):
    password = None
   # industry_match = forms.ChoiceField(choices=INDUSTRY_MATCH_CHOICE)
    rank_by = forms.MultipleChoiceField(required=False,
        choices=RANK_CHOICES)

    class Meta():
        model = Profile
        fields = {
            'industry_match',
            'rank_by',
        }

    def __init__(self, *args, **kwargs):
        super(MatchConfigurationForm, self).__init__(*args, **kwargs)
        if (self.instance.industry_choice_2 == 'None'):
            INDUSTRY_MATCH_CHOICE = [('Industry 1', self.instance.industry_choice_1),
                        ('Not Looking', 'Not Looking')]
        else:
            INDUSTRY_MATCH_CHOICE = [('Industry 1', self.instance.industry_choice_1),
                        ('Industry 2', self.instance.industry_choice_2),
                        ('Both', 'Both'),
                        ('Not Looking', 'Not Looking')]
        self.fields['industry_match'] = forms.ChoiceField(choices=INDUSTRY_MATCH_CHOICE)
    
