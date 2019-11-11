from django import forms

class TagForm(forms.Form):
  INDUSTRY_CHOICES = [('1', 'Tech'), ('2', 'Finance'), ('3', 'Consulting')]
  industry = forms.ChoiceField(widget=forms.SelectMultiple, choices=INDUSTRY_CHOICES)
