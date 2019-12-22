from django.contrib.auth.models import User
from onboard.models import Profile
from account.models import Statistics
from numpy.random import choice
import random
import math
from sys import stderr
from django.db.models import Q

year = {"Freshman":1,
        "Sophomore":2,
        "Junior":3,
        "Senior":4,
        "Graduate Student":5,
        "Postdoc":6,
        "Not in School": -1,
        "Unknown": -1}

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
    score += _second_industry_match(user_profile, match)
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

def _second_industry_match(user_profile, match):
    if (user_profile.industry_choice_2 == match.industry_choice_2):
        return 2.0
    
    return 0.0

def _normalize(p):
    sum = 0

    for val in p:
        sum += val

    p = list(map((lambda x: x / sum), p))

    return p

def _scoreIndustries(profile, match):
    GREAT_MATCH_BASE = 5.0
    MATCH_ADD = 2.0
    GOOD_MATCH_BASE = 4.0
    OKAY_MATCH_BASE = 3.0
    # Must be the case that profile.industry_choice_1 == match.industry_choice_1
    if (match.industry_match == 'Industry 1' and profile.industry_match == 'Industry 1'):
        score = GREAT_MATCH_BASE
        if (match.industry_choice_2 == profile.industry_choice_2):
            score += MATCH_ADD
    
    # Must be the case that profile.industry_choice_2 == match.industry_choice_2
    if (match.industry_match == 'Industry 2' and profile.industry_match == 'Industry 2'):
        score = GREAT_MATCH_BASE
        if (match.industry_choice_1 == profile.industry_choice_1):
            score += MATCH_ADD
    
    # Must be the case that profile.industry_choice_1 == match.industry_choice_2
    if (match.industry_match == 'Industry 2' and profile.industry_match == 'Industry 1'):
        score = GREAT_MATCH_BASE
        if (match.industry_choice_1 == profile.industry_choice_2):
            score += MATCH_ADD

    # Must be the case that profile.industry_choice_2 == match.industry_choice_1
    if (match.industry_match == 'Industry 1' and profile.industry_match == 'Industry 2'):
        score = GREAT_MATCH_BASE
        if (match.industry_choice_2 == profile.industry_choice_1):
            score += MATCH_ADD
    
    if (match.industry_match == 'Both' and profile.industry_match == 'Both'):
        if (profile.industry_choice_2 == match.industry_choice_2 and profile.industry_choice_1 == match.industry_choice_1):
            score = GREAT_MATCH_BASE + MATCH_ADD
        elif (profile.industry_choice_1 == match.industry_choice_2 and profile.industry_choice_2 == match.industry_choice_1):
            score = GREAT_MATCH_BASE 
        elif (profile.industry_choice_1 == match.industry_choice_1 or profile.industry_choice_2 == match.industry_choice_2):
            score = GOOD_MATCH_BASE
        elif (profile.industry_choice_1 == match.industry_choice_2 or profile.industry_choice_2 == match.industry_choice_1):
            score = OKAY_MATCH_BASE

    if (match.industry_match == 'Both' and profile.industry_match == 'Industry 1'):
        if (profile.industry_choice_1 == match.industry_choice_1):
            score = GOOD_MATCH_BASE
            if (profile.industry_choice_2 == match.industry_choice_2):
                score = GREAT_MATCH_BASE + MATCH_ADD
        elif (profile.industry_choice_1 == match.industry_choice_2):
            score = GOOD_MATCH_BASE
            if (profile.industry_choice_2 == match.industry_choice_1):
                    score = GREAT_MATCH_BASE + MATCH_ADD

    if (match.industry_match == 'Both' and profile.industry_match == 'Industry 2'):
        if (profile.industry_choice_2 == match.industry_choice_2):
            score = GOOD_MATCH_BASE
            if (profile.industry_choice_1 == match.industry_choice_1):
                score = GREAT_MATCH_BASE + MATCH_ADD
        elif (profile.industry_choice_2 == match.industry_choice_1):
            score = GOOD_MATCH_BASE
            if (profile.industry_choice_1 == match.industry_choice_2):
                    score = GREAT_MATCH_BASE + MATCH_ADD

    if (match.industry_match == 'Industry 1' and profile.industry_match == 'Both'):
        if (profile.industry_choice_1 == match.industry_choice_1):
            score = GREAT_MATCH_BASE
            if (profile.industry_choice_2 == match.industry_choice_2):
                score = GREAT_MATCH_BASE + MATCH_ADD
        elif (profile.industry_choice_2 == match.industry_choice_1):
            score = GOOD_MATCH_BASE
            if (profile.industry_choice_1 == match.industry_choice_2):
                    score = GOOD_MATCH_BASE + MATCH_ADD

    if (match.industry_match == 'Industry 2' and profile.industry_match == 'Both'):
        if (profile.industry_choice_2 == match.industry_choice_2):
            score = GREAT_MATCH_BASE
            if (profile.industry_choice_1 == match.industry_choice_1):
                score = GREAT_MATCH_BASE + MATCH_ADD
        elif (profile.industry_choice_1 == match.industry_choice_2):
            score = GOOD_MATCH_BASE
            if (profile.industry_choice_2 == match.industry_choice_1):
                    score = GOOD_MATCH_BASE + MATCH_ADD
        
    return score
            
        
def _scoreMostInterviews():
    pass

def _scoreRating():
    pass

def _getProfiles(profile, industryChoice):
    if (industryChoice == 'Industry 2' and profile.industry_choice_2 != 'None'):
        matchesList = Profile.objects.filter(
            # if (otherProfile.id != profile.id)
                # if (profile.industry2 == otherProfile.industry1 && otherProfile.industryMatch == 'Industry 1' or 'Both' OR
                #     profile.industry2 == otherProfile.industry2 && otherProfile.industryMatch == 'Industry 2' or 'Both')
            ~Q(id=profile.id), Q(is_matched=False), Q(Q(Q(industry_choice_1=profile.industry_choice_2), Q(Q(industry_match='Industry 1') | Q(industry_match='Both'))) |
             Q(Q(industry_choice_2=profile.industry_choice_2), Q(Q(industry_match='Industry 2') | Q(industry_match='Both'))))
            
            )
    elif (industryChoice == 'Both' and profile.industry_choice_2 != 'None'):
        matchesList = Profile.objects.filter(~Q(id=profile.id), Q(is_matched=False),
            # Combines the logic of the two other cases with an OR conditional
            Q(
            Q(Q(Q(industry_choice_1=profile.industry_choice_2), Q(Q(industry_match='Industry 1') | Q(industry_match='Both'))) |
             Q(Q(industry_choice_2=profile.industry_choice_2), Q(Q(industry_match='Industry 2') | Q(industry_match='Both'))))   
             
             |

             Q(Q(Q(industry_choice_1=profile.industry_choice_1), Q(Q(industry_match='Industry 1') | Q(industry_match='Both'))) |
             Q(Q(industry_choice_2=profile.industry_choice_1), Q(Q(industry_match='Industry 2') | Q(industry_match='Both')))) 
             )
        )
    else:
        matchesList = Profile.objects.filter(
            # if (otherProfile.id != profile.id)
                # if (profile.industry1 == otherProfile.industry1 && otherProfile.industryMatch == 'Industry 1' or 'Both' OR
                #     profile.industry1 == otherProfile.industry2 && otherProfile.industryMatch == 'Industry 2' or 'Both')
            ~Q(id=profile.id), Q(is_matched=False), Q(Q(Q(industry_choice_1=profile.industry_choice_1), Q(Q(industry_match='Industry 1') | Q(industry_match='Both'))) |
             Q(Q(industry_choice_2=profile.industry_choice_1), Q(Q(industry_match='Industry 2') | Q(industry_match='Both'))))
            
        )

    return matchesList

def _getNumInterviewsList(matchesList):
    numList = Statistics.objects.get(user=match.user).tot_interview

#----------------------------------------------------------------#
class MatchedUser(object):

    def __init__(self, score, user):
        self._user = user
        self._score = score
    
    def __lt__(self, other):
        return self._score < other._score

    def __gt__(self, other):
        return self._score > other._score

    def __eq__(self, other):
        return self._score == other._score

    def getUser(self):
        return self._user

def quick_match_prototype(profile):
    matches = Profile.objects.filter(industry=profile.industry_choice_1)
    matchesList = []

    for m in matches:
        if m.id is not profile.id:
            matchesList.append(m)

    if len(matchesList) is 0:
        return None

    randomMatch = random.randint(0, len(matchesList) - 1)

    return matchesList[randomMatch]

def list_match(profile, rankers, industryChoice):
    if (industryChoice == 'Not Looking'):
        return []

    matchesList = _getProfiles(profile, industryChoice)
    matchList = []

    if ('Most Interviews' in rankers):
        mostInterviewsList = _getNumInterviewsList(matchesList)

    for match in matchesList:
        score = 0.0
        if 'Industry' in rankers:
            score += _scoreIndustries(profile, match)
        if 'Role' in rankers:
            if match.role == profile.role:
                score += 1.0
        if 'Year in School' in rankers:
            score += _year_similarity(profile, match)
        if 'Similar Interviews' in rankers:
            score += _tot_interview_similarity(profile, match)
        if 'Most Interviews' in rankers:
            pass
        if 'Rating' in rankers:
            pass

        match = MatchedUser(score, match)
        matchList.append(match)

    matchList.sort(reverse=True)
    returnList = []
    for m in matchList:
        returnList.append(m.getUser())
    return returnList

def get_match_list(user_profile, recent_list):
    matchSet = _getProfiles(user_profile, user_profile.industry_match)
    
    # @Damon Does this need to be "pk"?
    # matchSet = matchSet.exclude(pk=user_profile.pk)

    print(len(matchSet))
    for recent_match in recent_list:
        matchSet = matchSet.exclude(user=recent_match.user)

    print(len(matchSet))
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
