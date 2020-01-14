from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.edit import FormMixin
from mockingbird.decorators import onboard_only

from django.views.generic import DetailView, ListView

from .forms import ComposeForm
from .models import Thread, ChatMessage
from account.pull_notif import pull_notif, mark_read
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
import json

@login_required(login_url='/login/')
@onboard_only
def open_chat(request):
    if request.method == 'POST' :#and 'markread' not in request.POST:
        username = request.POST.get('username')
        print(username)
        url = 'chat/' + username + "/"
        return redirect(url)
    ##elif request.method == 'POST' and 'markread' in request.POST:
     #   mark_read(request.user)

    else:
        print("not post")

class InboxView(LoginRequiredMixin, ListView):
    template_name = 'chat/inbox.html'
    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    login_url='/login/'
    template_name = 'chat/room.html'
    form_class = ComposeForm
    success_url = './'

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username  = self.kwargs.get("username")
        obj, created    = Thread.objects.get_or_new(self.request.user, other_username)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()

        pulled = pull_notif(self.request.user)
        context['has_unread'] = pulled[0]
        context['notif'] = pulled[1]
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if request.method == "POST" and 'markread' not in request.POST:
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        elif request.method == 'POST' and 'markread' in request.POST:
            mark_read(request.user)
            return self.form_invalid(form)

    def form_valid(self, form):
        thread = self.get_object()
        user = self.request.user
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=user, thread=thread, message=message)
        return super().form_valid(form)
