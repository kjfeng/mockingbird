from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

from .forms import FeedbackForm

# Create your views here.
@login_required(login_url='/login/')
def feedback(request):
    if request.method == 'POST':
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
            return render(request, 'feedback/feedback_complete.html')
    else:
        form = FeedbackForm()
        args = {'form': form}
        return render(request, 'feedback/feedback_form.html', args)