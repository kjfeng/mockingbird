"""mockingbird URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views

from django.conf.urls import url
from onboard import views as onboard_views
from match import views as match_views
from tags import views as tags_views
from chat import views as chat_views
from chat.views import ThreadView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    url(r'^signup/$', onboard_views.signup, name='signup'),
    url(r'^login/$', onboard_views.login, name='login'),

    url(r'^tags/$', tags_views.tags_view, name='tags'),
    path('', onboard_views.login, name='home'),

    path('chat/<str:username>/', ThreadView.as_view()),
    path('chat', chat_views.open_chat, name='open-chat'),
    #path('chat/<str:room_name>/', chat_views.room, name='room'),
    # re_path(r'^(?P<room_name>[^/]+)/$', chat_views.room, name='room'),
    # matching urls
    url(r'^match/$', match_views.match_view, name='match'),
    url(r'^matchresults/$', match_views.matchresults_view),
    url(r'^matchlist/$', match_views.matchlist_view, name='matchlist'),
    url(r'^matchlistresults/$', match_views.matchlistresults_view),
    url(r'^matchconfig/$', match_views.matchconfig_view, name='matchconfig'),
    url(r'^request_info/', match_views.request_info, name='request_info'),
    url(r'^accept_request/', match_views.accept_request, name='accept_request'),
    url(r'^confirm_cancel_request/', match_views.confirm_cancel_request, name='confirm_cancel_request'),
    url(r'^done_cancel/', match_views.done_cancel, name='done_cancel'),
    url(r'^send_request/$', match_views.send_request_home, name='send_request_home'),

    url(r'^account_activation_sent/$', onboard_views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        onboard_views.activate, name='activate'),
    url(r'^account/', include('account.urls')),
    url(r'^survey/', include(('survey.urls', 'survey'), namespace='survey')),
    url(r'^feedback/', include(('feedback.urls', 'feedback'), namespace='feedback')),
    url(r'^settings/', include(('settings.urls', 'settings'), namespace='settings')),

    url('^', include('django.contrib.auth.urls')),


    url(r'^(.*)', onboard_views.default_view, name='default'),

]
