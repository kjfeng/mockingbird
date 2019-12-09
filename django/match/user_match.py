from django.contrib.auth.models import User
from onboard.models import Profile
from account.models import Statistics
from numpy.random import choice
import random
import math
from sys import stderr

year = {"Freshman":1,
        "Sophomore":2,
        "Junior":3,
        "Senior":4,
        "Graduate Student":5,
        "Postdoc":6,
        "Not in School": -1}

#----------------------------------------------------------------#

def dequeue(my_list):
    if len(my_list) is 0:
        return 0

    my_list[0] = None

    return my_list[1:]

def enqueue(my_list, next_elem, max_size):
    if len(my_list) is max_size:
        my_list = dequeue(my_list)

    if next_elem not in my_list:
        my_list.append(next_elem)

    return my_list

#----------------------------------------------------------------#

def to_user_list(user_string):
    user_list = []

    if user_string is not None:
        user_list = user_string.split(",")

    if len(user_list) is 0:
        return user_list

    if "" in user_list:
        user_list.remove("")

    i = 0
    while i < len(user_list):
        username = user_list[i]
        user = User.objects.get(username=username)
        user_profile = Profile.objects.get(user=user)
        user_list[i] = user_profile
        i += 1

    return user_list

def to_user_string(user_list):
    user_string = ""

    for u in user_list:
        user_string += u.user.username + ","

    return user_string

#----------------------------------------------------------------#

def _calculate_score(user_profile, match):
    MIN_SCORE = 1
    matchStats = Statistics.objects.get(user=match.user)
    score = float(matchStats.rate)
    score += _tot_interview_similarity(user_profile, match)
    score += _year_similarity(user_profile, match)
    score += MIN_SCORE

    return score


def _tot_interview_similarity(user_profile, match):
    user_count = Statistics.objects.get(user=match.user).tot_interview
    match_count = Statistics.objects.get(user=match.user).tot_interview

    diff = math.fabs(user_count - match_count)

    if diff is 0:
        return 2.0
    elif diff <= 3:
        return 1.0
    else:
        return 0.0

def _year_similarity(user_profile, match):
    user_year = year.get(user_profile.year_in_school)
    match_year = year.get(match.year_in_school)

    if user_year == -1 or match_year == -1:
        return 0.0

    diff = float(math.fabs(user_year - match_year))

    return 1 - (diff / 6)

def _normalize(p):
    sum = 0

    for val in p:
        sum += val

    p = list(map((lambda x: x / sum), p))

    return p

#----------------------------------------------------------------#

def quick_match_prototype(profile):
    matches = Profile.objects.filter(industry=profile.industry)
    matchesList = []

    for m in matches:
        if m.id is not profile.id:
            matchesList.append(m)

    if len(matchesList) is 0:
        return None

    randomMatch = random.randint(0, len(matchesList) - 1)

    return matchesList[randomMatch]

def get_match_list(user_profile, recent_list):
    matchSet = Profile.objects.filter(industry=user_profile.industry, is_matched=False)
    matchSet = matchSet.exclude(pk=user_profile.pk)

    for recent_match in recent_list:
        matchSet = matchSet.exclude(user=recent_match.user)

    p = []

    for m in matchSet:
        score = _calculate_score(user_profile, m)
        p.append(score)

    if len(p) is 0:
        return None

    list_size = len(p)

    if len(p) > 10:
        list_size = 10

    p = _normalize(p)

    print(p, file=stderr)

    matchList = list(choice(matchSet, list_size, replace=False, p=p))

    # print(matchList, file=stderr)

    return matchList
