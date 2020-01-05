from django import forms


class ComposeForm(forms.Form):
    message = forms.CharField(
            required=False,
            widget=forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": 'Type message here.',
                }
                
                )
            )

    # Edit by bryan
    def __init__(self, *args, **kwargs):
        super(ComposeForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['message'].widget.attrs['style'] = 'width:70%; height:40px; input: focus {outline: none;}'