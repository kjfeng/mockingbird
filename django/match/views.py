from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
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
        messages.add_message(request, messages.INFO, str(match.email))
        messages.add_message(request, messages.INFO, str(match.industry))

    return redirect('../matchresults/')
    return render(request, "home.html", {})

def matchresults_view(request):
    storage = messages.get_messages(request)
    msgs = []
    username = ''
    email    = ''
    industry = ''


    for message in storage:
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

    return render(request, 'matching/matchresults.html', context)
