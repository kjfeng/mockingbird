from django import forms

class SurveyForm(forms.Form):
    MEETING_CHOICES = [('yes', 'Yes, I met with them!'), ('no', 'No, we were not able to meet :(')]
    did_meet = forms.ChoiceField(widget=forms.RadioSelect, choices=MEETING_CHOICES)

    TIME_CHOICES = [('good', 'On Time'), ('tardy', '< 10 minutes late'),
                    ('late', '10+ minutes late'), ('absent', 'No Show')]
    on_time = forms.ChoiceField(widget=forms.RadioSelect, choices=TIME_CHOICES)

    FRIEND_CHOICES = [('friendly', 'Very Friendly'), ('average', 'Friendly'), ('mid', 'No Impression'),
                      ('rude', 'Rude'), ('extreme', 'Extremely Rude')]
    friendly = forms.ChoiceField(widget=forms.RadioSelect, choices=FRIEND_CHOICES)

   # QUALITY_CHOICES = [('good', 'GOOD')]
   # quality = forms.ChoiceField(widget=forms.RadioSelect, choices=QUALITY_CHOICES)