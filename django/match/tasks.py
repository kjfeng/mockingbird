from __future__ import absolute_import, unicode_literals
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from celery import shared_task

from account.models import NotificationItem
@shared_task
def send_survey(request_user, target, current_site):
    print("sent email")
    # if the target has deleted their account, don't have to do this
    current_targets = User.objects.filter(username=target.username)
    if len(current_targets) == 0:
        return

    # if the survey has already been done, don't do this
    if request_user.profile.is_matched and request_user.profile.match_name == target.username:
        # logic to send email to the target
        subject = '[MockingBird] How was your Mock Interview?'
        message = render_to_string('matching/do_survey.html', {
            'user': request_user,
            'domain': current_site.domain,
        })
        request_user.profile.has_request = False
        request_user.profile.save()
        if request_user.profile.receive_email:
            request_user.email_user(subject, message)

        message = render_to_string('matching/do_survey.html', {
            'user': target,
            'domain': current_site.domain,
        })
        target.profile.is_sender = False
        target.profile.save()
        if target.profile.receive_email:
            target.email_user(subject, message)

@shared_task
def send_modal(request_user, target):
    print("sent modal")

    # if the target has deleted their account, don't have to do this
    current_targets = User.objects.filter(username=target.username)
    if len(current_targets) == 0:
        return

    # if the survey has already been done by current user, don't do this
    if request_user.profile.is_matched and request_user.profile.match_name == target.username:
        request_user.profile.send_survey = True
        request_user.profile.save()

    # if survey has been done by other user, don't do this
    if target.profile.is_matched and target.profile.match_name == request_user.username:
        target.profile.send_survey = True
        target.profile.save()


