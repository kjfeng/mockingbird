from onboard.models import Profile
from account.models import Statistics
from numpy.random import choice
import random
import math


year = {"Freshman":1,
        "Sophomore":2,
        "Junior":3,
        "Senior":4,
        "Graduate Student":5,
        "Postdoc":6,
        "Not in School": -1}

def _calculate_score(user_profile, match):
    score = Statistics.objects.get(pk=match.pk).avg_rate
    score += _tot_interview_similarity(user_profile, match)
    score += _year_similarity(user_profile, match)

    return score


def _tot_interview_similarity(user_profile, match):
    user_count = Statistics.objects.get(pk=user_profile.pk).tot_interview
    match_count = Statistics.objects.get(pk=match.pk).tot_interview

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

def getMatchList(user_profile):
    MATCH_LIST_SIZE = 10

    matchSet = Profile.objects.filter(industry=user_profile.industry, is_matched=False)
    p = []

    for m in matchSet:
        score = _calculate_score(m, user_profile)
        p.append(score)

    if len(p) is 0:
        return None

    #p = _normalize(p)

    matchList = choice(matchSet, MATCH_LIST_SIZE, replace=False, p=p)

    return matchList