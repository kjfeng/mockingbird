from __future__ import absolute_import, unicode_literals
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from celery import shared_task

@shared_task
def send_survey(request_user, target, current_site):
    # logic to send email to the target
    subject = '[MockingBird] How was your Mock Interview?'
    message = render_to_string('matching/do_survey.html', {
        'user': request_user,
        'domain': current_site.domain,
    })
    request_user.profile.has_request = False
    request_user.profile.save()
    request_user.email_user(subject, message)

    message = render_to_string('matching/do_survey.html', {
        'user': target,
        'domain': current_site.domain,
    })
    target.profile.is_sender = False
    target.profile.save()
    target.email_user(subject, message)
