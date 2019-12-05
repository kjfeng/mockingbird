from django.shortcuts import render, redirect
from sys import stderr

from .forms import SurveyForm

def survey(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST)

        if form.is_valid():
            #form.save()
            #print("here", file=stderr)
            return redirect('survey:survey_complete')
    else:
        form = SurveyForm()
        args = {'form': form}
        return render(request, 'survey/survey.html', args)


def survey_complete(request):
    return render(request, 'survey/survey_complete.html')