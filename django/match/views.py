from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from onboard.models import Profile
from .user_match import quick_match_prototype
from sys import stderr

# Create your views here.
def match_view(request):
    # if request.method == 'POST':
    #     print(request.POST)
    #     # clear messages
    #     storage = messages.get_messages(request)
    #     for message in storage:
    #         str(message)
    #
    #     my_profile = Profile.objects.get(id=request.user.id)
    #     match = quick_match_prototype(my_profile)
    #
    #     if match is not None:
    #         messages.add_message(request, messages.INFO, str(match.user.username))
    #         messages.add_message(request, messages.INFO, str(match.email))
    #         messages.add_message(request, messages.INFO, str(match.industry))
    #
    #     return redirect('../matchresults/')

    # clear messages
    storage = messages.get_messages(request)
    for message in storage:
        str(message)

    my_profile = Profile.objects.get(id=request.user.id)
    match = quick_match_prototype(my_profile)

    if match is not None:
        messages.add_message(request, messages.INFO, str(match.user.username))
        messages.add_message(request, messages.INFO, str(match.user.email))
        messages.add_message(request, messages.INFO, str(match.industry))

    return redirect('../matchresults/')
    #return render(request, "home.html", {})

def matchresults_view(request):
    storage = messages.get_messages(request)
    msgs = []
    username = ''
    email    = ''
    industry = ''

    for message in storage:
        print(message, file=stderr)
        msgs.append(message)

    if len(msgs) > 0:
        username = msgs[0]
        email    = msgs[1]
        industry = msgs[2]
        messages.add_message(request, messages.INFO, username)
        messages.add_message(request, messages.INFO, email)
        messages.add_message(request, messages.INFO, industry)

    context = {
        'msgs': msgs,
        'username': username,
        'email': email,
        'industry': industry
    }

    if request.method == 'POST':
        #print(context['username'])
        t_username = context['username']

        # change sender to blocked
        request.user.profile.is_matched = True
        request.user.profile.is_waiting = True
        request.user.profile.match_name = str(username)
        request.user.profile.save()

        # change target's settings
        target = User.objects.filter(username=str(t_username))[0]
        #print(target[0],file=stderr)

        target.profile.match_name = request.user.username
        target.profile.is_matched = True
        target.profile.has_request = True
        target.profile.save()

        # logic to send email to the target
        current_site = get_current_site(request)
        subject = '[MockingBird] You have a Match!'
        message = render_to_string('matching/matching_email.html', {
            'user': target,
            'domain': current_site.domain,
        })
        target.email_user(subject, message)

        return redirect('request_info')

    return render(request, 'matching/matchresults.html', context)


def request_info(request):
    target = User.objects.filter(username=request.user.profile.match_name)[0]
    context = {
        'username': target.username,
        'industry': target.profile.industry,
        'year': target.profile.year_in_school,
        'role': target.profile.role
    }

    return render(request, 'matching/request_info.html', context)


def confirm_cancel_request(request):
    target = User.objects.filter(username=request.user.profile.match_name)[0]

    context = {
        'username': target.username,
    }
    return render(request, 'matching/confirm_cancel.html', context)


def done_cancel(request):
    target = User.objects.filter(username=request.user.profile.match_name)[0]
    target.profile.match_name = ""
    target.profile.is_matched = False
    target.profile.has_request = False
    target.profile.save()

    request.user.profile.is_matched = False
    request.user.profile.match_name = ""
    request.user.profile.is_waiting = False
    request.user.profile.save()

    context = {
        'username': target.username,
    }
    return render(request, 'matching/done_cancel.html', context)
