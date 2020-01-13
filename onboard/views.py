# Create your views here.
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from account.pull_notif import pull_notif, mark_read
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.core.mail import EmailMessage
from sys import stderr


from .tokens import account_activation_token
from .forms import SignUpForm, ForgotPasswordForm, LoginForm
from match.views import match_view, matchlist_get, _on_accept_home


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            # print("hello")
            user.save()
            # print("yay")
            current_site = get_current_site(request)
            subject = 'Activate Your Mockingbird Account'
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


def login(request):
    pulled = pull_notif(request.user)
    if request.method == 'POST' and 'markread' in request.POST:
        mark_read(request.user)
        pulled = pull_notif(request.user)

    discover_users = []
    recommended = None

    if request.user.id is not None:
        matchlist = matchlist_get(request)
        length = len(matchlist)
        length = 3 if length > 3 else length

        if length > 0:
            for x in range(length):
                if not matchlist[x].profile.is_idle:
                    if recommended is not None:
                        discover_users.append(matchlist[x])
                    else:
                        recommended = matchlist[x]


    match = ""
    requested_users = []

    if not request.user.is_anonymous:
        if request.user.profile.match_name != "" and request.user.profile.match_name != "None":
            name = request.user.profile.match_name
            match = User.objects.filter(username=name)[0]

        if request.user.profile.is_matched or request.user.profile.is_waiting or request.user.profile.has_request:

            requested_names = str(request.user.profile.requested_names).split(",")
            # requested_users = []

            for name in requested_names:
                if name is not '':
                    requested_users.append(User.objects.get(username=name))



    context = {
        'has_unread': pulled[0],
        'notif': pulled[1],
        'discover_users': discover_users,
        'recommended': recommended,
        'match': match,
        'users': requested_users,
    }

    if request.method == 'POST' and 'send_request' in request.POST:
        _on_accept_home(request, discover_users[0])
        return redirect('home')

    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                # return invalid login error message
                return render(request, '../templates/home.html', {'form': form, 'error_message': "Incorrect username and/or password"})
    else:
        form = LoginForm()
    context['form'] = form
    return render(request, '../templates/home.html', context=context)

def default_view(request, extra):
    pulled = pull_notif(request.user)

    if request.method == 'POST' and 'markread' in request.POST:
        mark_read(request.user)
        pulled = pull_notif(request.user)

    return render(request, '../templates/broken_page.html', {'has_unread': pulled[0], 'notif': pulled[1]})
'''
def forgotPassword(request):
    # print(request.method)
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(email=form.cleaned_data['email'])[0]
            current_site = get_current_site(request)

            subject = 'Reset Your Mockingbird Password'
            message = render_to_string('registration/password_reset_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            user.email_user(subject, message)
            return redirect('password_reset_sent')
    else:
        form = ForgotPasswordForm()
    return render(request, '../templates/registration/password_reset_form.html', {'form': form})


def password_reset_sent(request):
    return render(request, 'registration/password_reset_done.html')


def password_reset(request):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):

        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return redirect('change_password')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = PasswordChangeForm(request.user)

        return render(request, 'accounts/change_password.html', {
            'form': form
        })
    else:
        return render(request, 'registration/account_activation_invalid.html')
'''
