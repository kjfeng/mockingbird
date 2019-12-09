from onboard.models import Profile
import random

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
    matches = Profile.objects.filter(industry=profile.industry)
    matchesList = []

    for m in matches:
        if m.id is not profile.id:
            matchesList.append(m)

    if len(matchesList) is 0:
        return None

    randomMatch = random.randint(0, len(matchesList) - 1)

    return matchesList[randomMatch]

def list_match(profile, preferences):
    matches = Profile.objects.all()
    matchesList = []
    
    for m in matches:
        if m.id is not profile.id:
            matchesList.append(m)

    # if len(matches) is 0:
    #     return None

    usersList = []

    for user in matchesList:
        print("user seen")
        score = 0
        if 'Industry' in preferences:
            if user.industry == profile.industry:
                score += 1
        if 'Role' in preferences:
            if user.role == profile.role:
                score += 1
        if 'Year in School' in preferences:
            if user.year_in_school == profile.year_in_school:
                score += 1
        
        user = MatchedUser(score, user)
        usersList.append(user)

    usersList.sort(reverse=True)
    returnList = []
    for m in usersList:
        returnList.append(m.getUser())
    return returnList

    
        
        

    