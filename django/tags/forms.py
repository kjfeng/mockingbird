from django.contrib.auth.forms import UserChangeForm
from django import forms
from django.contrib.auth.models import User

from onboard.models import Profile, INDUSTRY_CHOICES, INDUSTRY_MATCH_CHOICE



class TagForm(UserChangeForm):
  industry_choice_1 = forms.ChoiceField(choices=INDUSTRY_CHOICES)
  industry_choice_2 = forms.ChoiceField(choices=INDUSTRY_CHOICES)
  industry_match = forms.ChoiceField(choices=INDUSTRY_MATCH_CHOICE)
  password = None
  class Meta:
    model = Profile
    fields = {
      'industry_choice_1',
      'industry_choice_2',
      'industry_match',
    }

  def is_valid(self):
     
        # run the parent validation first
        valid = super(TagForm, self).is_valid()
 
        # we're done now if not valid
        if not valid:
            return valid

        if (self.cleaned_data['industry_choice_1'] == self.cleaned_data['industry_choice_2']):
            return False

        if (self.cleaned_data['industry_choice_1'] == 'None' or self.cleaned_data['industry_choice_1'] == None):
            return False
 
        # all good
        return True
