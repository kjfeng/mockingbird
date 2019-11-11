from django import forms

class TagForm(forms.Form):
  INDUSTRY_CHOICES = [('tech', 'Tech'), ('finance', 'Finance'), ('consulting', 'Consulting')]
  industry = forms.MultipleChoiceField(choices=INDUSTRY_CHOICES)
