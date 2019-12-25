from django.shortcuts import render, redirect
from account.pull_notif import pull_notif
from .forms import SettingsForm

# Create your views here.
def settings(request):
    pulled = pull_notif(request.user)
    if request.method == 'POST' and 'markread' in request.POST:
        for x in pulled[1]:
            x.read = True
            x.save()
    context = {
        'has_unread': pulled[0],
        'notif': pulled[1]
    }
    return render(request, 'settings/settings.html', context)

def edit_settings(request):
    pulled = pull_notif(request.user)

    if request.method == "POST" and 'markread' not in request.POST:
        form = SettingsForm(request.user)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        if request.method == 'POST' and 'markread' in request.POST:
            for x in pulled[1]:
                x.read = True
                x.save()

        form = SettingsForm(request.user)
        context = {
            'form': form,
            'has_unread': pulled[0],
            'notif': pulled[1]
            }
        return render(request, 'settings/settings_form.html', context)
