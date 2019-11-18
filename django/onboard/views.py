# Create your views here.
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


from .tokens import account_activation_token
from .forms import SignUpForm, ForgotPasswordForm, LoginForm
from match.views import match_view


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MockingBird Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
        else:
          error_message=''
          username = request.POST['username']
          try:
            user = User.objects.get(username=username)
          except:
            error_message = "We encountered a problem signing you up"
          return render(request, 'registration/signup.html', {'form': form, 'error_message':error_message})

    else:
        form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
            else:
                # return invalid login error message
                return render(request, '../templates/home.html', {'form': form, 'error_message': "Incorrect username and/or password"})
    else:
        form = LoginForm()
    return render(request, '../templates/home.html', {'form': form})

def forgotPassword(request):
    print(request.method)
    if request.method == 'post':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = ForgotPasswordForm()
    return render(request, '../templates/registration/password_reset_form.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.profile.email = user.email
        user.save()
        return redirect('home')
    else:
        return render(request, 'registration/account_activation_invalid.html')
