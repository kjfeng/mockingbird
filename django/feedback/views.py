from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

from .forms import FeedbackForm
from account.pull_notif import pull_notif, mark_read

# Create your views here.
@login_required(login_url='/login/')
def feedback(request):
    pulled = pull_notif(request.user)

    if request.method == 'POST' and 'markread' not in request.POST:
        form = FeedbackForm(request.POST)

        if form.is_valid():
            if form.cleaned_data['feedback'] != "":
                subject = 'Feedback Left'
                message = form.cleaned_data['feedback'] + "\n from <b>" + str(request.user.username) + "</b>"
                send_mail(
                    subject,
                    message,
                    'teammockingbird333@gmail.com',
                    ['teammockingbird333@gmail.com'],
                    fail_silently=True,
                )
            context = {
                'has_unread': pulled[0],
                'notif': pulled[1]
            }
            return render(request, 'feedback/feedback_complete.html', context)
    else:
        if request.method == 'POST' and 'markread' in request.POST:
            mark_read(request.user)
            pulled = pull_notif(request.user)

        form = FeedbackForm()
        args = {'form': form,
            'has_unread': pulled[0],
            'notif': pulled[1]
        }
        return render(request, 'feedback/feedback_form.html', args)