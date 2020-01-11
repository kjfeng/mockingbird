from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from onboard.models import ERROR_MESSAGES
from mockingbird.decorators import onboard_only
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .models import NotificationItem

from django.urls import reverse
import sys


from .forms import EditAccountForm, EditProfileForm
from .pull_notif import pull_notif
from match.views import matchlist_create, _on_accept_home

# Create your views here.
@login_required(login_url='/login/')
@onboard_only
def account_details(request):
    pulled = pull_notif(request.user)
    context = {
        'has_unread':pulled[0],
        'notif': pulled[1]
    }
    return render(request, 'account/profile_page.html', context)

@login_required(login_url='/login/')
def account_delete(request):
    pulled = pull_notif(request.user)
    context = {
        'has_unread': pulled[0],
        'notif': pulled[1]
    }
    return render(request, 'account/confirm_delete_user.html', context)


def account_delete_confirm(request):
    if request.user.profile.match_name and request.user.profile.match_name != "None":
        target = User.objects.get(username=request.user.profile.match_name)

        # refreshes the list
        matchlist_create(target)

        # case where they were actually matched with their partner
        if request.user.profile.is_matched:
            # send notification to the target about their partner being deleted
            NotificationItem.objects.create(type="DA", user=target, match_name=str(request.user.username))

            current_site = get_current_site(request)

            # logic to send email to the target
            if target.profile.receive_email:
                subject = '[MockingBird] Your Match has Deleted Their Account :('
                message = render_to_string('account/deleted_user_email.html', {
                    'user': target,
                    'deleted_user': request.user.username,
                    'domain': current_site.domain,
                })
                target.email_user(subject, message)

            # reset target's profile
            target.profile.is_matched = False
            target.profile.match_name = "None"
            target.profile.save()

        else:
            # if they only sent a request, reset the requested info
            request_names = target.profile.requested_names
            names_array = request_names.split(",")
            new_array = []
            for name in names_array:
                if name != request.user.username:
                    new_array.append(name)

            target.profile.requested_names = ",".join(new_array)
            target.profile.save()

    # case where the partner only sent a request
    names_list = request.user.profile.requested_names.split(",")
    for name in names_list:
        target = User.objects.filter(username=name)

        # if the target no longer in database skip
        if len(target) == 0:
            continue

        target = target[0]

        # logic to unmatch partner
        target.profile.match_name = "None"
        target.profile.is_waiting = False
        target.profile.is_sender = False
        target.profile.save()

        # send them a notification
        NotificationItem.objects.create(type="DAR", user=target, match_name=str(request.user.username))

        # send them an email
        if target.profile.receive_email:
            current_site = get_current_site(request)
            subject = '[MockingBird] Your Match Request has Deleted Their Account :('
            message = render_to_string('account/deleted_user_email.html', {
                'user': target,
                'deleted_user': request.user.username,
                'domain': current_site.domain,
            })
            target.email_user(subject, message)

    request.user.delete()

    return render(request, 'account/deleted_user.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required(login_url='/login')
@onboard_only
def account_edit(request):
    initial_data = {
        'year_in_school': request.user.profile.year_in_school,
        'industry_choice_1': request.user.profile.industry_choice_1,
        'industry_choice_2': request.user.profile.industry_choice_2,
        'industry_match': request.user.profile.industry_match,
        'major': request.user.profile.major,
        'role': request.user.profile.role,
        'summary': request.user.profile.summary
    }
    obj = request.user.profile
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)
        formB = EditProfileForm(request.POST, instance=request.user.profile)
        isBValidReturn = formB.is_valid()
        if form.is_valid() and isBValidReturn == 1:
            form.save()
            formB.save()
            matchlist_create(request.user)
            return redirect('account:account_details')
        else:
            formB.fields['role'].label = "Desired Role"
            formB.fields['industry_match'].label = "What industry would you prefer to be matched on?"
            formB.fields['summary'].label = "Description"

            error_message = 'You can\'t fly just yet! ' + ERROR_MESSAGES[isBValidReturn]
            pulled = pull_notif(request.user)
            args = {'form': form,
                'formB': formB,
                'has_unread': pulled[0],
                'notif': pulled[1],
                'error_message': error_message}
            return render(request, 'account/edit_profile.html', args)
    else:
        form = EditAccountForm(instance=request.user)
        formB = EditProfileForm(instance=request.user.profile, initial=initial_data)

        formB.fields['role'].label = "Desired Role"
        formB.fields['industry_match'].label = "What industry would you prefer to be matched on?"
        formB.fields['summary'].label = "Description"

        pulled = pull_notif(request.user)
        args = {'form': form,
                'formB': formB,
                'has_unread': pulled[0],
                'notif': pulled[1],
                'error_message': ''}
        return render(request, 'account/edit_profile.html', args)


@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')

            current_site = get_current_site(request)

            # send an email that also says this
            if request.user.profile.receive_email:
                subject = '[MockingBird] Your Password has been Changed!'
                message = render_to_string('account/changed_password_email.html', {
                    'user': request.user,
                    'domain': current_site.domain,
                })
                request.user.email_user(subject, message)

            return redirect('account:account_details')
        else:
            messages.error(request, 'Please correct the error below.')

    else:
        form = PasswordChangeForm(request.user)
    pulled = pull_notif(request.user)
    context = {
        'form': form,
        'has_unread': pulled[0],
        'notif': pulled[1]
    }
    return render(request, 'account/change_password.html', context)

@login_required(login_url='/login')
@onboard_only
def show_statistics(request):
    ranking = 1
    if request.user.statistics.tot_interview >= 25 and request.user.statistics.overall_rating >= 4:
        ranking = 4
    elif request.user.statistics.tot_interview >= 10 and request.user.statistics.overall_rating >= 4:
        ranking = 3
    elif request.user.statistics.tot_interview >= 5 and request.user.statistics.overall_rating >= 4:
        ranking = 2

    total_late = request.user.statistics.late * request.user.statistics.tot_interview
    pulled = pull_notif(request.user)
    context = {
        'tot_late': total_late,
        'has_unread': pulled[0],
        'notif': pulled[1],
        'ranking': ranking
    }
    if request.method == 'POST' and 'markread' in request.POST:
        for x in pulled[1]:
            x.read = True
            x.save()
    return render(request, 'account/stat_page.html', context)

@login_required(login_url='/login')
@onboard_only
def profile_view(request, username):
    has_sent = False
    is_matched = False
    match_name = request.user.profile.match_name

    print(username)
    print(match_name)
    if request.user.profile.is_matched and match_name == username:
        print("both")
        is_matched = True
        has_sent = True
    elif match_name == username:
        print("request")
        has_sent = True
    elif match_name != "" and match_name != "None":
        print("is matched")
        is_matched = True
    u = User.objects.filter(username=username)

    pulled = pull_notif(request.user)

    context = {
        'user': request.user,
        'target_user': u,
        'has_unread': pulled[0],
        'notif': pulled[1],
        'has_sent': has_sent,
        'is_matched': is_matched,
    }
    if len(u) == 0:
        return render(request, 'broken_page.html', context)
    context['target_user'] = u[0]

    if request.method == 'POST' and 'markread' in request.POST:
        for x in pulled[1]:
            x.read = True
            x.save()

    elif request.method == 'POST' and 'send_request' in request.POST:
        print(u[0].username)
        valid = _on_accept_home(request, u[0].username)
        context['has_sent'] = True
        if valid:
            return render(request, 'account/profile_view.html', context)
        else:
            return render(request, 'account/profile_does_not_exist.html', context)

    return render(request, 'account/profile_view.html', context)


''' to be implemented once multiple request sent
@login_required(login_url='/login')
def send_request(request, username):
    u = User.object.get(username=username)
'''