from django.contrib.auth.forms import UserChangeForm
from django import forms
from django.contrib.auth.models import User

from onboard.models import Profile, INDUSTRY_CHOICES, INDUSTRY_MATCH_CHOICE, YEAR_IN_SCHOOL_CHOICES


class BasicForm(UserChangeForm):
    year_in_school = forms.ChoiceField(choices=YEAR_IN_SCHOOL_CHOICES)
    major = forms.CharField(required=False, widget=forms.Textarea(
        attrs={"rows": 1, "cols": 50}))

    role = forms.CharField(required=False, widget=forms.Textarea(
        attrs={"rows": 1, "cols": 50}))

    summary = forms.CharField(required=False, widget=forms.Textarea(
        attrs={"rows":10, "cols": 20}
    ))

    password = None

    class Meta:
        model = Profile
        fields = {
            'year_in_school',
            'major',
            'role',
            'summary'
        }

class TagForm(UserChangeForm):
  industry_choice_1 = forms.CharField(widget=forms.Select(choices=INDUSTRY_CHOICES), help_text="Choose your preferred/primary industry.")
  industry_choice_2 = forms.CharField(widget=forms.Select(choices=INDUSTRY_CHOICES), help_text="If you would also like to interview for another industry, choose your secondary industry.")
  industry_match = forms.CharField(widget=forms.Select(choices=INDUSTRY_MATCH_CHOICE), help_text="Choose which of your chosen industries you'd like to be matched in. Or find matches in both (or neither)!")
  password = None
  class Meta:
    model = Profile
    fields = [
      'industry_choice_1',
      'industry_choice_2',
      'industry_match'
    ]

  def is_valid(self):

        # run the parent validation first
        valid = super(TagForm, self).is_valid()

        # we're done now if not valid
        if not valid:
            return valid

        if (self.cleaned_data['industry_choice_1'] == 'None' or self.cleaned_data['industry_choice_1'] == None):
            return 'No Industry 1'

        if (self.cleaned_data['industry_choice_1'] == self.cleaned_data['industry_choice_2']):
            return 'Dup Industry'

        if (self.cleaned_data['industry_choice_2'] == 'None' and (self.cleaned_data['industry_match'] == 'Industry 2' or self.cleaned_data['industry_match'] == 'Both')):
            return 'Industry Match'



        # all good
        return 1
