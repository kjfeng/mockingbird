from django import forms

class SurveyForm(forms.Form):
    MEETING_CHOICES = [('yes', 'Yes, I met with them!'), ('no', 'No, we were not able to meet :(')]
    did_meet = forms.ChoiceField(widget=forms.RadioSelect, choices=MEETING_CHOICES)

    TIME_CHOICES = [('4', 'On Time'), ('3', '< 10 minutes late'),
                    ('2', '10+ minutes late'), ('1', 'No Show')]
    on_time = forms.ChoiceField(widget=forms.RadioSelect, choices=TIME_CHOICES)

    FRIEND_CHOICES = [('5', 'Very Friendly'), ('4', 'Friendly'), ('3', 'No Impression'),
                      ('2', 'Rude'), ('1', 'Extremely Rude')]
    friendly = forms.ChoiceField(widget=forms.RadioSelect, choices=FRIEND_CHOICES)

    # QUALITY_CHOICES = [('good', 'GOOD')]
   # quality = forms.ChoiceField(widget=forms.RadioSelect, choices=QUALITY_CHOICES)
    class Meta:
        fields = ('did_meet', 'on_time', 'friendly')
