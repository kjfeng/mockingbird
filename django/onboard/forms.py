from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# add whatever other info we want to add
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'username', 'email',
            'password1', 'password2')