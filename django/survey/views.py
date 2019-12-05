from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from sys import stderr
from decimal import *

from .forms import SurveyForm

def survey(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST)

        if form.is_valid():
            target = User.objects.filter(username=request.user.profile.match_name)[0]
            print(target, file=stderr)
            print(target.profile.industry, file=stderr)
            if form.cleaned_data['did_meet'] == 'no':
                print("did not meet", file=stderr)
                target.statistics.no_show += 1
                target.statistics.save()
            else:
                print("did meet", file=stderr)

                # update on_time
                target.statistics.tot_interview += 1
                current_total_rate = Decimal(target.statistics.rate)*target.statistics.tot_interview
                target.statistics.rate = (current_total_rate + Decimal(form.cleaned_data['friendly'])/Decimal(5.0))/target.statistics.tot_interview

                current_total_late = Decimal(target.statistics.late)*target.statistics.tot_interview
                target.statistics.late += (current_total_late + Decimal(form.cleaned_data['friendly'])/Decimal(5.0))/target.statistics.tot_interview
                target.statistics.save()

                request.user.profile.is_matched = False;
                request.user.save()
            return redirect('survey:survey_complete')
    else:
        form = SurveyForm()
        args = {'form': form}
        return render(request, 'survey/survey.html', args)


def survey_complete(request):
    return render(request, 'survey/survey_complete.html')