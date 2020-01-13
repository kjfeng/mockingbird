from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# add whatever other info we want to add
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'username', 'email',
            'password1', 'password2', )
        help_text = {
            'password2': 'why isnt this working',
        }

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error('email', "This email is already in use!")
        return self.cleaned_data


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter email to receive password resetting instructions.')

    class Meta:
        fields = ('email',)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        fields = ('username', 'password',)
