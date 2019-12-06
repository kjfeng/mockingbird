from django import forms

class FeedbackForm(forms.Form):
    feedback = forms.CharField(max_length=1000, required=True)

    class Meta:
        fields = ('feedback')
