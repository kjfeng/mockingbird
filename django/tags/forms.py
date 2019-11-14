from django import forms

class TagForm(forms.Form):
  INDUSTRY_CHOICES = [('Technology', 'Technology'), ('Finance', 'Finance'), ('Consulting', 'Consulting')]
  industry = forms.MultipleChoiceField(choices=INDUSTRY_CHOICES)
