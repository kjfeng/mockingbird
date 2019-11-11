from onboard.models import Profile
import random

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