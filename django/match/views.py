from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from onboard.models import Profile
from django.contrib.auth.decorators import login_required
from .user_match import quick_match_prototype, list_match
from sys import stderr

from .forms import MatchConfigurationForm

class MatchedUser(object):
    def __init__(self, username: str, email: str, industry: str):
        self.username = username
        self.email = email
        self.industry = industry  
    
    def getUsername(self):
        return self.username

    def getEmail(self):
        return self.email

    def getIndustry(self):
        return self.industry

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
        matchedUser = MatchedUser(username = str(match.user.username), email = str(match.user.email),
                       industry = str(match.industry))
        request.session['matchedUser'] = matchedUser.__dict__

    return redirect('../matchresults/')
    return render(request, "home.html", {})

def matchresults_view(request):
    matchedUser = request.session.get('matchedUser', None)
    matchedUsers = []
    if matchedUser is not None:
        request.session['matchedUser'] = matchedUser
        matchedUsers.append(matchedUser)

    context = {
        'matchedUsers': matchedUsers,
    }

    return render(request, 'matching/matchresults.html', context)

def matchlist_view(request):
    my_profile = Profile.objects.get(id=request.user.id)
    form = MatchConfigurationForm(request.POST)
    preferences = []
    if form.is_valid():
        print("Here")
        for f in form.cleaned_data['filter_by']:
            preferences.append(f)


    #print(preferences)
    # if (data.get('Industry') is not None):
    #     preferences.append(data.get('Industry'))
    # if (data.get('Role') is not None):
    #     preferences.append(data.get('Role'))
    # if (data.get('Year In School') is not None):
    #     preferences.append(data.get('Year in School'))
    matches = list_match(my_profile, preferences)
    # print(preferences[0])
    matchedUsers = []
    for match in matches:
        matchedUser = MatchedUser(username = str(match.user.username), email = str(match.user.email),
                       industry = str(match.industry))
        matchedUsers.append(matchedUser.__dict__)
   
    request.session['matchedUsers'] = matchedUsers

    return redirect('../matchlistresults/')

def matchlistresults_view(request):
    matchedUsers = request.session.get('matchedUsers', None)
    context = {
        'matchedUsers': matchedUsers
    }

    return render(request, 'matching/matchresults.html', context)

def matchconfig_view(request):
    if request.method == 'POST':
        form = MatchConfigurationForm(request.user, request.POST)
        if form.is_valid():
            return render(request, 'matching/match.html', {'form': form})
        else:
            messages.error(request, 'An error occurred with loading page')

    else:
        form = MatchConfigurationForm()
    return render(request, 'matching/match.html', {'form': form})
    


