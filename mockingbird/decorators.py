from functools import wraps
from django.shortcuts import redirect


def onboard_only(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.profile.onboard_confirmed:
            return function(request, *args, **kwargs)
        else:
            return redirect('home')
    return wrap