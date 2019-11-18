from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# add whatever other info we want to add
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True,
                             help_text='Required.')

    class Meta:
        model = User
        fields = ('username', 'email', 
            'password1', 'password2', )

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter email to receive password resetting instructions.')

    class Meta:
        fields = ('email',)

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        fields = ('username', 'password',)
