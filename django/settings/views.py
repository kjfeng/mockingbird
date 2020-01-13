from django.shortcuts import render, redirect
from account.pull_notif import pull_notif
from .forms import SettingsForm
from match.views import matchlist_create

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
        form = SettingsForm(request.POST, instance=request.user.profile)

        if form.is_valid():
            form.save()
            return redirect('settings:settings')
    else:
        form = SettingsForm(instance=request.user.profile)

    form['receive_email'].label = "Do you want to receive email notifications from Mockingbird?"
    form['is_idle'].label = "Do you want to be inactive?"
    form['is_idle'].help_text = "(You will not be able to match nor will you show up in other user's recommended matches.)"


    if request.method == 'POST' and 'markread' in request.POST:
        for x in pulled[1]:
            x.read = True
            x.save()

    context = {
        'form': form,
        'has_unread': pulled[0],
        'notif': pulled[1]
        }
    return render(request, 'settings/settings_form.html', context)
