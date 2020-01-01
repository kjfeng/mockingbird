from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

from onboard.models import Profile, YEAR_IN_SCHOOL_CHOICES, INDUSTRY_CHOICES, INDUSTRY_MATCH_CHOICE

class EditAccountForm(UserChangeForm):
    password = None
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    class Meta:
        model = User
        fields = {
            'email',
            'first_name'
        }

class EditProfileForm(UserChangeForm):
    year_in_school = forms.ChoiceField(choices=YEAR_IN_SCHOOL_CHOICES)

    industry_choice_1 = forms.ChoiceField(choices=INDUSTRY_CHOICES)
    
    industry_choice_2 = forms.ChoiceField(choices=INDUSTRY_CHOICES)

    industry_match = forms.ChoiceField(choices=INDUSTRY_MATCH_CHOICE)

    major = forms.CharField(required=False, widget=forms.Textarea(
        attrs={"rows":1, "cols":50}))

    role = forms.CharField(required=False, widget=forms.Textarea(
        attrs={"rows":1,"cols":50}))

    password = None

    class Meta:
        model = Profile
        fields = [
            'year_in_school',
            'major',
            'role',
            'industry_choice_1',
            'industry_choice_2',
            'industry_match',
        ]
    
    def is_valid(self):
         
        # run the parent validation first
        valid = super(EditProfileForm, self).is_valid()
 
        # we're done now if not valid
        if not valid:
            return valid

        if (self.cleaned_data['industry_choice_1'] == self.cleaned_data['industry_choice_2']):
            return 'Dup Industry'

        if (self.cleaned_data['industry_choice_1'] == 'None' or self.cleaned_data['industry_choice_1'] == None):
            return 'No Industry 1'
 
        if (self.cleaned_data['industry_choice_2'] == 'None' and (self.cleaned_data['industry_match'] == 'Industry 2' or self.cleaned_data['industry_match'] == 'Both')):
            return 'Industry Match'

        
       
        # all good
        return 1
