from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from sys import stderr
from decimal import *
from chat.models import Thread
from django.db.models import Q
from .forms import SurveyForm
from account.pull_notif import pull_notif, mark_read
from mockingbird.decorators import onboard_only
from match.views import matchlist_create


@login_required(login_url='/login/')
@onboard_only
def survey(request):
    pulled = pull_notif(request.user)

    # if not matched
    if not request.user.profile.is_matched:
        context = {
            'has_unread': pulled[0],
            'notif': pulled[1]
        }
        if request.method == 'POST' and 'markread' in request.POST:
            mark_read(request.user)
            pulled = pull_notif(request.user)
            context['has_unread'] = pulled[0]
            context['notif'] = pulled[1]

        return render(request, 'survey/no_survey.html', context)

    # if submitted
    if request.method == 'POST' and 'markread' not in request.POST:
        form = SurveyForm(request.POST)
        # if valid form
        if form.is_valid():
            target = User.objects.filter(username=request.user.profile.match_name)[0]

            # update information about user
            request.user.profile.match_name = ""
            request.user.profile.is_matched = False
            request.user.profile.send_survey = False

            # now that multiple request don't need this?
            request.user.profile.is_sender = False
            request.user.profile.is_waiting = False
            request.user.profile.save()

            # update information about user's match
            # if tried to meet but the other person did not show up
            if form.cleaned_data['did_meet'] == 'yes' and form.cleaned_data['on_time'] == '1':
                target.statistics.no_show += 1
                target.statistics.overall_rating -= Decimal(0.5)
                target.statistics.save()
            elif form.cleaned_data['did_meet'] == 'yes':
                # print("did meet", file=stderr)

                # update the target's statistics
                current_total_rate = Decimal(target.statistics.rate) * target.statistics.tot_interview

                target.statistics.rate = (current_total_rate + Decimal(form.cleaned_data['friendly']))/(target.statistics.tot_interview +1)
                target.statistics.tot_interview += 1

                # adding late
                if form.cleaned_data['on_time'] == "2" or form.cleaned_data['on_time'] == "3":
                    target.statistics.late += 1

                # updates to ratings
                if form.cleaned_data['friendly'] == "2":
                    target.statistics.overall_rating -= Decimal(0.2)

                elif form.cleaned_data['friendly'] == "1":
                    target.statistics.overall_rating -= Decimal(0.1)
                target.statistics.save()

                if form.cleaned_data['on_time'] == "2":
                    target.statistics.overall_rating -= Decimal(0.1)
                elif form.cleaned_data['on_time'] == "3":
                    target.statistics.overall_rating -= Decimal(0.2)
                target.statistics.save()

                # positive updates (capped at 5)
                if target.statistics.overall_rating < 5:
                    if form.cleaned_data['on_time'] == "4" and form.cleaned_data['friendly'] == "4":
                        target.statistics.overall_rating += Decimal(0.1)
                    elif form.cleaned_data['on_time'] == "4" and form.cleaned_data['friendly'] == "5":
                        target.statistics.overall_rating += Decimal(0.2)
                target.statistics.save()

                # send email if there is feedback
                if form.cleaned_data['comment'] != "":
                    subject = 'Comment Left'
                    message = form.cleaned_data['comment'] + "\n from <b>" + str(
                        request.user.username) + "</b> for " + str(target.username)
                    send_mail(
                        subject,
                        message,
                        'teammockingbird333@gmail.com',
                        ['teammockingbird333@gmail.com'],
                        fail_silently=True,
                    )

            Thread.objects.filter(Q(first=request.user) | Q(second=request.user)).delete()
            matchlist_create(request.user)
            return redirect('survey:survey_complete')

    # if first time loading
    else:
        form = SurveyForm()

    form.fields['did_meet'].label = "Did you meet with your match?"
    form.fields['on_time'].label = "Was your match on time?"
    form.fields['friendly'].label = "How friendly or rude was your match?"
    form.fields['comment'].label = "If you have any additional comments or concern you would like to mention about " \
                                   "your partner, please add below."

    form.fields['did_meet'].initial = 'n/a'

    if request.method == 'POST' and 'markread' in request.POST:
        mark_read(request.user)
        pulled = pull_notif(request.user)

    args = {
        'form': form,
        'username': str(request.user.profile.match_name),
        'has_unread': pulled[0],
        'notif': pulled[1]
    }
    return render(request, 'survey/survey.html', args)


@login_required(login_url='/login/')
@onboard_only
def survey_complete(request):
    pulled = pull_notif(request.user)

    if request.method == 'POST' and 'markread' in request.POST:
        mark_read(request.user)
        pulled = pull_notif(request.user)

    context = {
        'has_unread': pulled[0],
        'notif': pulled[1]
    }
    return render(request, 'survey/survey_complete.html', context)
