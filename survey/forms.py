from django import forms

#from .models import Post_Survey

MEETING_CHOICES = [('n/a', 'Please select an answer'), ('yes', 'Yes, we did try to meet'), ('no', 'No, we did not try to meet')]
TIME_CHOICES = [('n/a', 'Please select an answer'), ('4', 'On Time'), ('3', '< 10 minutes late'),
                    ('2', '10+ minutes late'), ('1', 'No Show')]
FRIEND_CHOICES = [('n/a', 'Please select an answer'), ('5', 'Very Friendly'), ('4', 'Friendly'), ('3', 'No Impression'),
                      ('2', 'Rude'), ('1', 'Extremely Rude')]


class SurveyForm(forms.Form):
    did_meet = forms.CharField(widget=forms.Select(choices=MEETING_CHOICES))

    on_time = forms.CharField(widget=forms.Select(choices=TIME_CHOICES))

    friendly = forms.CharField(widget=forms.Select(choices=FRIEND_CHOICES))

    comment = forms.CharField(max_length=500, required=False, widget=forms.Textarea(attrs={'cols': 10, 'rows': 10}))

    class Meta:
        #model = Post_Survey
        fields = ['did_meet', 'on_time', 'friendly', 'comment']

    def clean(self):
        cleaned_data = super(SurveyForm, self).clean()
        did_meet = cleaned_data.get("did_meet")
        if did_meet == 'n/a':
            raise forms.ValidationError({'did_meet': ["This field is required.",]})

        # did_meet is toggled, make the other fields required
        elif did_meet == 'yes':
          on_time = cleaned_data.get("on_time")
          friendly = cleaned_data.get("friendly")
          msg = forms.ValidationError("This field is required.")
          if on_time == 'n/a':
            self.add_error('on_time', msg)
          if friendly == 'n/a':
            self.add_error('friendly', msg)

        return cleaned_data
