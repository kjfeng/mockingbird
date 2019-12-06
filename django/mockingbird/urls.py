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
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views

from django.conf.urls import url
from onboard import views as onboard_views
from match import views as match_views
from tags import views as tags_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    url(r'^signup/$', onboard_views.signup, name='signup'),
    url(r'^login/$', onboard_views.login, name='login'),

    path('tags/', tags_views.tags_view),
    path('', onboard_views.login, name='home'),

    # matching urls
    path('match/', match_views.match_view, name='match'),
    path('matchresults/', match_views.matchresults_view),
    url(r'^request_info/', match_views.request_info, name='request_info'),
    url(r'^accept_request/', match_views.accept_request, name='accept_request'),
    url(r'^confirm_cancel_request/', match_views.confirm_cancel_request, name='confirm_cancel_request'),
    url(r'^done_cancel/', match_views.done_cancel, name='done_cancel'),

    url(r'^account_activation_sent/$', onboard_views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        onboard_views.activate, name='activate'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^survey/', include(('survey.urls', 'survey'), namespace='survey')),

]
