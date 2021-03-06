from django import template
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from onboard.models import Profile
from .models import Cached_Matches, Recent_Matches, Cached_List_Matches
from .user_match import quick_match_prototype, get_match_list, list_match
from .user_match import to_user_list, to_user_string, dequeue, enqueue
from sys import stderr
from .tasks import send_survey
from datetime import timedelta
from django.utils import timezone
from .forms import MatchConfigurationForm
#from post_office import mail

from account.models import NotificationItem
from account.pull_notif import pull_notif, mark_read
from mockingbird.decorators import onboard_only

class MatchedUser(object):
    def __init__(self, username: str, email: str, industry1: str, industry2: str, year: str):
        self.username = username
        self.email = email
        if industry2 == 'None':
            self.industry = industry1
        else:
            self.industry = industry1 + ', ' + industry2
        self.year = year

    def getUsername(self):
        return self.username

    def getEmail(self):
        return self.email

    def getIndustry(self):
        return self.industry

    def getYear(self):
        return self.year

register = template.Library()

def _on_accept_home(request, username):
    if request.method == 'POST':
        t_username = username

        target = User.objects.filter(username=str(t_username))[0]
        if not target: return False

        print(t_username)
        # change sender to blocked
        request.user.profile.is_waiting = True
        request.user.profile.match_name = str(t_username)
        request.user.profile.is_sender = True
        request.user.profile.save()
        request.user.profile.request_name = str(t_username)

        # change target's info


        target.profile.requested_names = target.profile.requested_names + "," + request.user.username
        #target.profile.is_matched = True
        target.profile.is_sender = False
        target.profile.is_waiting = False
        target.profile.has_request = True
        target.profile.save()

        current_site = get_current_site(request)

        # logic to send email to the target if user accepts emails
        if target.profile.receive_email:
            subject = '[MockingBird] You have a Match!'
            message = render_to_string('matching/matching_email.html', {
                'user': target,
                'domain': current_site.domain,
            })
            target.email_user(subject, message)

        # logic to create a notification for the target
        NotificationItem.objects.create(type="MR", user=target, match_name=str(request.user.username))
        return True

def _on_accept(request):
    if request.method == 'POST':
        t_username = request.POST.get('username')

        # change sender to blocked
        request.user.profile.is_waiting = True
        request.user.profile.match_name = str(t_username)
        request.user.profile.is_sender = True
        request.user.profile.save()
        request.user.profile.request_name = str(t_username)

        # change target's info
        target = User.objects.filter(username=str(t_username))[0]

        target.profile.requested_names = target.profile.requested_names + "," + request.user.username
        #target.profile.is_matched = True
        target.profile.is_sender = False
        target.profile.is_waiting = False
        target.profile.has_request = True
        target.profile.save()

        current_site = get_current_site(request)
        # logic to send email to the target if user accepts emails
        if target.profile.receive_email:
            subject = '[MockingBird] You have a Match!'
            message = render_to_string('matching/matching_email.html', {
                'user': target,
                'domain': current_site.domain,
            })
            target.email_user(subject, message)

        # logic to create a notification for the target
        NotificationItem.objects.create(type="MR", user=target, match_name=str(request.user.username))
        return True

# Create your views here.
@login_required(login_url='/login/')
@onboard_only
def match_view(request):
    L_SIZE = 10

    # # clear messages
    ## storage = messages.get_messages(request)
    # for message in storage:
    #      str(message)
    # clear messages
    storage = messages.get_messages(request)
    for message in storage:
         str(message)

    my_profile = Profile.objects.get(id=request.user.id)

    recent = Recent_Matches.objects.get(user=my_profile.user)
    recent_list = to_user_list(recent.matches, 'p')
    print(type(recent_list))

    match_cache = Cached_Matches.objects.get(user=my_profile.user)
    match_cache_list = to_user_list(match_cache.matches, 'p')

    # if has a deleted user remake it
    #if match_cache_list == "Deleted User":
    #    matchlist_create(request.user)
    #    match_cache = Cached_Matches.objects.get(user=my_profile.user)
    #    match_cache_list = to_user_list(match_cache.matches, 'p')

    match_list = match_cache_list
    if len(match_list) is 0:
        match_list = get_match_list(my_profile, recent_list)
    print(match_list)
    # match = quick_match_prototype(my_profile)
    if match_list is not None and len(match_list) is not 0:
        print("here")
        match = User.objects.get(username=match_list[0])
        match_profile = Profile.objects.get(user=match)

        recent_list = enqueue(recent_list, match_profile, L_SIZE)
        recent.matches = to_user_string(recent_list)
        recent.save()

        matchedUser = MatchedUser(username = str(match.username),
                                  email = str(match.email),
                                  industry1 = str(match.profile.industry_choice_1),
                                  industry2 = str(match.profile.industry_choice_2),
                                  year=str(match.profile.year_in_school))
        request.session['matchedUser'] = matchedUser.__dict__

        match_list = dequeue(match_list)
        match_cache.matches = to_user_string(match_list)
        match_cache.save()
        print("cache after matching: " + match_cache.matches, file=stderr)
    else:
        request.session['matchedUser'] = None

    return redirect('../matchresults/')

# @login_required
# def matchagain_view(request):
#     my_profile = Profile.objects.get(id=request.user.id)

#     match_cache = Cached_Matches.objects.get(user=my_profile.user)
#     match_cache_list = to_user_list(match_cache.matches)


@login_required(login_url='/login/')
@onboard_only
def matchresults_view(request):
    '''
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
    '''

    matchedUser = request.session.get('matchedUser', None)
    matchedUsers = []
    if matchedUser is not None:
        request.session['matchedUser'] = matchedUser
        matchedUsers.append(matchedUser)

    pulled = pull_notif(request.user)

    context = {#
        #'msgs': msgs,
        #'username': username,
        #'email': email,
        #'industry': industry,
        'has_unread': pulled[0],
        'notif': pulled[1],
        'matchedUsers': matchedUsers,
        'configured': False
    }
    if request.method == 'POST' and 'markread' in request.POST:
        mark_read(request.user)
        pulled = pull_notif(request.user)
        context['has_unread'] = pulled[0]
        context['notif'] = pulled[1]
    else:
        val_acceptance = _on_accept(request)
        if (val_acceptance):
            # requested_names = str(request.user.profile.requested_names) + request.POST.get('username') + ","
            # request.user.profile.requested_names = requested_names
            # request.user.profile.save()
            return redirect('request_info')

    return render(request, 'matching/matchresults.html', context)

@login_required(login_url='/login/')
@onboard_only
def matchlist_view(request):
    if request.method == 'POST':
        # my_profile = Profile.objects.get(id=request.user.id)
        # form = MatchConfigurationForm(request.POST, instance=request.user.profile)

        # rankers = []
        # industryChoice = 'Industry 1'
        # if form.is_valid():
        #     form.save()
        #     rankers = request.POST.getlist('rank_by')
        #     industryChoice = request.POST.get('industry_match')

        # matches = list_match(my_profile, rankers, industryChoice)
        my_profile = Profile.objects.get(id=request.user.id)
        rankersString = str(my_profile.rank_by)

        rankers = []
        if (rankersString is not None):
            rankers = rankersString.split(',')

        if "" in rankers:
            rankers.remove("")
        match_list = list_match(my_profile, rankers, my_profile.industry_match)
        matches = to_user_string(match_list)
        match_cache = Cached_List_Matches.objects.filter(user=my_profile.user)
        if (len(match_cache) == 0):
            match_cache = Cached_List_Matches.objects.create(user=my_profile.user, matches=matches)
        else:
            match_cache = list(match_cache)[0]
            match_cache.matches = matches

        match_cache.save()

        matchedUsers = []
        for match in match_list:
            matchedUser = MatchedUser(username = str(match.user.username), email = str(match.user.email),
                    industry1 = str(match.industry_choice_1), industry2 = str(match.industry_choice_2), year=str(match.year_in_school))
            matchedUsers.append(matchedUser.__dict__)

        request.session['matchedUsers'] = matchedUsers
    else:
        return redirect('home')

    return redirect('../matchlistresults/')

# Creats a list match caching
def matchlist_create(user):
    my_profile = user.profile
    rankers = my_profile.rank_by

    match_list = list_match(my_profile, rankers, my_profile.industry_match)
    matches = to_user_string(match_list)
    match_cache = Cached_List_Matches.objects.filter(user=my_profile.user)
    if (len(match_cache) == 0):
        match_cache = Cached_List_Matches.objects.create(user=my_profile.user, matches=matches)
    else:
        match_cache = list(match_cache)[0]
        match_cache.matches = matches

    match_cache.save()


# Grabs the cache match list for the given user
def matchlist_get(request):
    my_profile = Profile.objects.get(id=request.user.id)
    match_cache = Cached_List_Matches.objects.filter(user=my_profile.user)

    # in the case that the user doesn't have a cached match list yet
    if not match_cache:
        matchlist_create(request.user)

    match_cache = Cached_List_Matches.objects.filter(user=my_profile.user)[0]

    match_cache_list = to_user_list(match_cache.matches, 'u')

    # If there is a deleted user in the cache, refresh cache then return the new cache list.
    if match_cache_list == 'Deleted User':
        matchlist_create(request.user)
        match_cache = Cached_List_Matches.objects.filter(user=my_profile.user)[0]
        match_cache_list = to_user_list(match_cache.matches, 'u')

    return match_cache_list

@login_required(login_url='/login/')
@onboard_only
def matchlistresults_view(request):
    matchedUsers = request.session.get('matchedUsers', None)
    pulled = pull_notif(request.user)
    if request.method == 'POST' and 'markread' in request.POST:
        mark_read(request.user)
        pulled = pull_notif(request.user)

    context = {
        'has_read': pulled[0],
        'notif': pulled[1],
        'matchedUsers': matchedUsers,
        'configured': True
    }

    val_acceptance = _on_accept(request)
    if (val_acceptance):
        return redirect('request_info')
    return render(request, 'matching/matchresults.html', context)

@login_required(login_url='/login/')
@onboard_only
def matchconfig_view(request):
    initial_data = {
        'industry_match': request.user.profile.industry_match,
        'rank_by': request.user.profile.rank_by,
    }

    form = MatchConfigurationForm(instance=request.user.profile, initial=initial_data)
    form.fields['industry_match'].label = "Which industry or industries are you looking to be matched on?"
    form.fields['rank_by'].label = "Which fields do you want to rank your matches by? (Ctrl or Cmd + Click) to select multiple."


    pulled = pull_notif(request.user)

    if request.method == 'POST' and 'markread' in request.POST:
        mark_read(request.user)
        pulled = pull_notif(request.user)

    return render(request, 'matching/match.html', {'form': form,
                                                   'has_unread': pulled[0],
                                                   'notif': pulled[1]})

@login_required(login_url='/login/')
@onboard_only
def update_matchconfig(request):
    if request.method == 'POST':
        my_profile = Profile.objects.get(id=request.user.id)
        form = MatchConfigurationForm(request.POST, instance=request.user.profile)

        if form.is_valid():
            form.save()
            matchlist_create(request.user)
        else:
            return redirect('matchconfig')

    return redirect('home')

@login_required(login_url='/login/')
@onboard_only
def request_info(request):
    pulled = pull_notif(request.user)

    if request.user.profile.is_matched or request.user.profile.is_waiting or request.user.profile.has_request:

        requested_names = str(request.user.profile.requested_names).split(",")
        requested_users = []

        for name in requested_names:
            if name is not '':
                requested_users.append(User.objects.get(username=name))

        if request.method == 'POST' and 'markread' in request.POST:
            mark_read(request.user)
            pulled = pull_notif(request.user)

        requestee = request.session.get('matchedUser', None)

        request_match = ""
        request_matches = User.objects.filter(username=request.user.profile.match_name)
        if request_matches:
            request_match = request_matches[0]

        # if (str(target.profile.industry_choice_2) == 'None'):
        #     industry = target.profile.industry_choice_1
        # else:
        #     industry = str(target.profile.industry_choice_1) + ', ' + str(target.profile.industry_choice_2)
        context = {
            'users': requested_users,
            'requestee': requestee,
            'request_match': request_match,
            # 'username': target.username,
            # 'industry': industry,
            # 'year': target.profile.year_in_school,
            # 'role': target.profile.role,
            # 'email': target.email,
            'has_unread': pulled[0],
            'notif': pulled[1],
            'request': request
        }

        return render(request, 'matching/request_info.html', context)
    else:
        if request.method == 'POST' and 'markread' in request.POST:
            mark_read(request.user)
            pulled = pull_notif(request.user)

        context = {
            'has_unread': pulled[0],
            'notif': pulled[1]
        }

        return render(request, 'matching/no_request.html', context)

@login_required(login_url='/login/')
@onboard_only
def accept_request(request):
    if not request.user.profile.has_request:
        pulled = pull_notif(request.user)

        if request.method == 'POST' and 'markread' in request.POST:
            mark_read(request.user)
            pulled = pull_notif(request.user)

        context = {
            'has_unread': pulled[0],
            'notif': pulled[1]
        }
        return render(request, 'matching/no_request.html', context)
    else:
        t_username = request.POST.get('match')
        requested_users = str(request.user.profile.requested_names).split(",")
        print("t_username: " + t_username, file=stderr)

        # change target's settings
        for name in requested_users:
            if name == "":
                continue
            print("requested user: " + name, file=stderr)
            target = User.objects.get(username=name)
            if t_username == name:
                target.profile.is_matched = True
                target.profile.match_name = request.user.username
                print("this user is a match", file=stderr)
            else:
                target.profile.is_matched = False
                target.profile.match_name = ""
                print("this user is not a match", file=stderr)
            target.profile.is_waiting = False
            target.profile.is_sender = False
            target.profile.save()

        # change sender and accepter to matched
        request.user.profile.is_matched = True
        request.user.profile.has_request = False
        request.user.profile.requested_names = ""
        request.user.profile.match_name = t_username
        request.user.profile.save()


        # make notification item for target
        NotificationItem.objects.create(type="MA", user=target, match_name=str(request.user.username))
        current_site = get_current_site(request)

        # logic to send email to the target
        if target.profile.receive_email:
            subject = '[MockingBird] Your Match has been confirmed!'
            message = render_to_string('matching/match_confirmed.html', {
                'user': target,
                'domain': current_site.domain,
            })
            target.email_user(subject, message)

        #send_survey(request, target, str(target.profile.match_name), str(t_username))
        send_time = timezone.now() + timedelta(seconds=30)
        #send_survey.apply_async(eta=send_time, args=(request.user, target, current_site))
        send_survey.apply_async(eta=send_time, args=(request.user, target, current_site))

        matchedUser = MatchedUser(username = str(target.username),
                                  email = str(target.email),
                                  industry1 = str(target.profile.industry_choice_1),
                                  industry2 = str(target.profile.industry_choice_2),
                                  year = str(target.profile.year_in_school))

        # notification for the send survey notification


        request.session['matchedUser'] = matchedUser.__dict__
        return redirect('request_info')

@login_required(login_url='/login/')
@onboard_only
def confirm_cancel_request(request):
    match = None
    if request.user.profile.is_sender and request.user.profile.is_waiting:
        match = request.user.profile.match_name
    else:
        match = request.POST.get('match')

    # if match accepted/declined request already
    if match == None:
      match = request.user.profile.match_name

      # if match declined
      if not match:
        return render(request, 'matching/done_cancel.html')

      # if match accepted
      target = User.objects.get(username=match)
      email = target.email
      #print("hello match:", match, email)
      context = {
          'match': match,
          'email': email,
      }
      return render(request, 'matching/cannot_cancel.html', context)

    target = User.objects.get(username=match)
    pulled = pull_notif(request.user)
    print("my match")


    if request.method == 'POST' and 'markread' in request.POST:
        mark_read(request.user)
        pulled = pull_notif(request.user)

    context = {
        'username': target.username,
        'has_unread': pulled[0],
        'notif': pulled[1],
        'match': match,
    }
    return render(request, 'matching/confirm_cancel.html', context)


@login_required(login_url='/login/')
@onboard_only
def done_cancel(request):
    if request.method == 'POST' and 'markread' in request.POST:
        storage = messages.get_messages(request)
        msgs = []
        for m in storage:
            msgs.append(m)
        mark_read(request.user)
        pulled = pull_notif(request.user)

        context = {
            'username': msgs[0],
            'has_unread': pulled[0],
            'notif': pulled[1],
        }
        return render(request, 'matching/done_cancel.html', context)

    # update target's info
    match = request.POST.get('match')
    target = User.objects.get(username=match)

    # case where they're trying to go to this url forcefully
    if not match or match == "None":
        return redirect('../default')

    # make a notification for the target
    # if user is sender, they are canceling
    if request.user.profile.is_sender:
        # update own info
        request.user.profile.is_waiting = False
        request.user.profile.is_sender = False
        request.user.profile.match_name = "None"
        request.user.save()

        # print("here")
        # if they are only one in the request
        request_names = target.profile.requested_names.split(",")
        if len(request_names) == 0:
            target.profile.has_request = False
        else:
            # remove their name from request_names
            new_names = []
            for x in request_names:
                if x and x != request.user.username:
                    new_names.append(x)
            if len(new_names) == 0:
                target.profile.has_request = False
                target.profile.requested_names = ""
            else:  # else reset the names
                target.profile.requested_names = ",".join(new_names)

        if target.profile.receive_email:
            # send email that the match has been rejected
            subject = '[MockingBird] Canceled Match Request :('
            message = render_to_string('matching/cancel_email.html', {
                'user': target,
                'cancel_username': request.user.username,
            })
            target.email_user(subject, message)

        matchlist_create(request.user)
        NotificationItem.objects.create(type="MC", user=target, match_name=str(request.user.username))

    # if user is not the sender, they are rejecting someone
    else:
        target.profile.is_sender = False
        target.profile.is_waiting = False
        target.profile.match_name = ""

        # update current user
        requested_names = str(request.user.profile.requested_names).split(",")
        new_names = []
        for x in requested_names:
            if x and x != target.username:
                print(x)
                new_names.append(x)
        # print("rejecting")
        # print(new_names)


        # if none remaining, change to false
        if len(new_names) == 0:
            request.user.profile.has_request = False
            request.user.profile.requested_names = ""
        else: #else reset the names
            request.user.profile.requested_names = ",".join(new_names)

        # send email
        if target.profile.receive_email:
            # send email that the match has been rejected
            subject = '[MockingBird] Rejected Match Request :('
            message = render_to_string('matching/reject_email.html', {
                'user': target,
                'cancel_username': request.user.username,
            })
            target.email_user(subject, message)

        NotificationItem.objects.create(type="MD", user=target, match_name=str(request.user.username))
    target.profile.save()
    request.user.profile.save()

    pulled = pull_notif(request.user)

    context = {
        'username': target.username,
        'has_unread': pulled[0],
        'notif': pulled[1],
    }

    messages.add_message(request, messages.INFO, str(target.username))


    return render(request, 'matching/done_cancel.html', context)

def send_request_home(request):
    _on_accept(request)
    return redirect('home')
