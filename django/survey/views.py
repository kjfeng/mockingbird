from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from sys import stderr
from decimal import *

from .forms import SurveyForm


@login_required(login_url='/login/')
def survey(request):
    if not request.user.profile.is_matched:
        return render(request, 'survey/no_survey.html')

    if request.method == 'POST':
        form = SurveyForm(request.POST)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from sys import stderr
from decimal import *

from .forms import SurveyForm


@login_required(login_url='/login/')
def survey(request):
    if not request.user.profile.is_matched:
        return render(request, 'survey/no_survey.html')

    if request.method == 'POST':
        form = SurveyForm(request.POST)

        if form.is_valid():
            target = User.objects.filter(username=request.user.profile.match_name)[0]
            #print(target, file=stderr)
            #print(target.profile.industry, file=stderr)

            # update information about user
            request.user.profile.match_name = ""
            request.user.profile.is_matched = False
            request.user.profile.save()

            # update information about user's match
            if form.cleaned_data['did_meet'] == 'no':
                #print("did not meet", file=stderr)
                target.statistics.no_show += 1
                target.statistics.save()
            else:
                #print("did meet", file=stderr)

                # update the target's statistics
                target.statistics.tot_interview += 1
                current_total_rate = Decimal(target.statistics.rate)*target.statistics.tot_interview
                target.statistics.rate = (current_total_rate + Decimal(form.cleaned_data['friendly'])/Decimal(5.0))/target.statistics.tot_interview

                current_total_late = Decimal(target.statistics.late)*target.statistics.tot_interview
                target.statistics.late += (current_total_late + Decimal(form.cleaned_data['friendly'])/Decimal(5.0))/target.statistics.tot_interview
                target.statistics.save()

                # send email if there is feedback
                if form.cleaned_data['comment'] != "":
                    subject = 'Comment Left'
                    message = form.cleaned_data['comment'] + "\n from <b>" + str(request.user.username) + "</b>"
                    send_mail(
                        subject,
                        message,
                        'teammockingbird333@gmail.com',
                        ['teammockingbird333@gmail.com'],
                        fail_silently=True,
                    )
            return redirect('survey:survey_complete')
    else:
        form = SurveyForm()
        form.fields['did_meet'].label = "Did you meet with your match?"
        form.fields['on_time'].label = "Was your match on time?"
        form.fields['friendly'].label = "How friendly or rude was your match?"
        form.fields['comment'].label = "If you have any additional comments or concern you would like to mention about" \
                                       "your partner, please add below."

        args = {
            'form': form,
            'username': str(request.user.profile.match_name),
        }
        return render(request, 'survey/survey.html', args)


@login_required(login_url='/login/')
def survey_complete(request):
    return render(request, 'survey/survey_complete.html')
    if form.is_valid():
        target = User.objects.filter(username=request.user.profile.match_name)[0]
        #print(target, file=stderr)
        #print(target.profile.industry, file=stderr)

        # update information about user
        request.user.profile.match_name = ""
        request.user.profile.is_matched = False
        request.user.save()

        # update information about user's match
        if form.cleaned_data['did_meet'] == 'no':
            #print("did not meet", file=stderr)
            target.statistics.no_show += 1
            target.statistics.save()
        else:
            #print("did meet", file=stderr)

            # update the target's statistics
            target.statistics.tot_interview += 1
            current_total_rate = Decimal(target.statistics.rate)*target.statistics.tot_interview
            target.statistics.rate = (current_total_rate + Decimal(form.cleaned_data['friendly'])/Decimal(5.0))/target.statistics.tot_interview

            current_total_late = Decimal(target.statistics.late)*target.statistics.tot_interview
            target.statistics.late += (current_total_late + Decimal(form.cleaned_data['friendly'])/Decimal(5.0))/target.statistics.tot_interview
            target.statistics.save()

            # send email if there is feedback
            if form.cleaned_data['comment'] != "":
                subject = 'Comment Left'
                message = form.cleaned_data['comment'] + "\n from <b>" + str(request.user.username) + "</b>"
                send_mail(
                    subject,
                    message,
                    'teammockingbird333@gmail.com',
                    ['teammockingbird333@gmail.com'],
                    fail_silently=True,
                )
        return redirect('survey:survey_complete')
    else:
        form = SurveyForm()
        form.fields['did_meet'].label = "Did you meet with your match?"
        form.fields['on_time'].label = "Was your match on time?"
        form.fields['friendly'].label = "How friendly or rude was your match?"
        form.fields['comment'].label = "If you have any additional comments or concern you would like to mention about" \
                                       "your partner, please add below."

        args = {
            'form': form,
            'username': str(request.user.profile.match_name),
        }
        return render(request, 'survey/survey.html', args)


@login_required(login_url='/login/')
def survey_complete(request):
    return render(request, 'survey/survey_complete.html')
