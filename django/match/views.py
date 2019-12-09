from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from onboard.models import Profile
from .models import Cached_Matches, Recent_Matches
from .user_match import quick_match_prototype, get_match_list
from .user_match import to_user_list, to_user_string, dequeue, enqueue
from sys import stderr

# Create your views here.
@login_required(login_url='/login/')
def match_view(request):
    L_SIZE = 10
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

    recent = Recent_Matches.objects.get(user=my_profile.user)
    recent_list = to_user_list(recent.matches)

    match_cache = Cached_Matches.objects.get(user=my_profile.user)
    match_cache_list = to_user_list(match_cache.matches)

    match_list = match_cache_list
    if len(match_list) is 0:
        match_list = get_match_list(my_profile, recent_list)

    # match = quick_match_prototype(my_profile)
    if match_list is not None and len(match_list) is not 0:
        match = User.objects.get(username=match_list[0])
        match_profile = Profile.objects.get(user=match)

        recent_list = enqueue(recent_list, match_profile, L_SIZE)
        recent.matches = to_user_string(recent_list)
        recent.save()

        messages.add_message(request, messages.INFO, str(match.username))
        messages.add_message(request, messages.INFO, str(match.email))
        messages.add_message(request, messages.INFO, str(match_profile.industry))

        match_list = dequeue(match_list)
        match_cache.matches = to_user_string(match_list)
        match_cache.save()
        print("cache after matching: " + match_cache.matches, file=stderr)

    return redirect('../matchresults/')

@login_required(login_url='/login/')
def matchresults_view(request):
    storage = messages.get_messages(request)
    msgs = []
    username = ''
    email    = ''
    industry = ''

    for message in storage:
        # print(message, file=stderr)
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
        request.user.profile.is_sender = True
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


@login_required(login_url='/login/')
def request_info(request):
    if not request.user.profile.is_matched:
        return render(request, 'matching/no_request.html')
    else:
        target = User.objects.filter(username=request.user.profile.match_name)[0]
        context = {
            'username': target.username,
            'industry': target.profile.industry,
            'year': target.profile.year_in_school,
            'role': target.profile.role
        }

        return render(request, 'matching/request_info.html', context)


@login_required(login_url='/login/')
def confirm_cancel_request(request):
    target = User.objects.filter(username=request.user.profile.match_name)[0]

    context = {
        'username': target.username,
    }
    return render(request, 'matching/confirm_cancel.html', context)


@login_required(login_url='/login/')
def done_cancel(request):

    # update target's info
    target = User.objects.filter(username=request.user.profile.match_name)[0]
    target.profile.match_name = ""
    target.profile.is_matched = False
    target.profile.has_request = False
    target.profile.save()

    # send email that the match has been canceled
    subject = '[MockingBird] Canceled Match :('
    message = render_to_string('matching/cancel_email.html', {
        'user': target,
        'cancel_username': request.user.username,
    })
    target.email_user(subject, message)

    # update current user's info
    request.user.profile.is_matched = False
    request.user.profile.match_name = ""
    request.user.profile.is_waiting = False
    request.user.profile.save()

    context = {
        'username': target.username,
    }
    return render(request, 'matching/done_cancel.html', context)
