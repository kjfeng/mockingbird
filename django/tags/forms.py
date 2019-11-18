from django.contrib.auth.forms import UserChangeForm
from django import forms
from django.contrib.auth.models import User

from onboard.models import Profile, INDUSTRY_CHOICES



class TagForm(UserChangeForm):
  industry = forms.MultipleChoiceField(choices=INDUSTRY_CHOICES)
  password = None
  class Meta:
    model = Profile
    fields = {
      'industry',
    }
