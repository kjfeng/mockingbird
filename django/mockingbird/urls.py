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
    #url(r'^ForgotPassword/$', onboard_views.forgotPassword, name='forgotPassword'),
    #url(r'reset_password_sent/$', onboard_views.password_reset_sent, name='password_reset_sent'),
    #url(r'reset_password_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #   onboard_views.password_reset, name='password_reset_confirm'),

    path('tags/', tags_views.tags_view),
    path('', onboard_views.login, name='home'),
    path('match/', match_views.match_view, name='match'),
    path('matchresults/', match_views.matchresults_view),
    path('matchlist/', match_views.matchlist_view, name='matchlist'),
    path('matchlistresults/', match_views.matchlistresults_view),
    path('matchconfig/', match_views.matchconfig_view, name='matchconfig'),
    url(r'^account_activation_sent/$', onboard_views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        onboard_views.activate, name='activate'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^account/', include('account.urls')),
]
'''
    url(r'^user/password/reset/$',
        'django.contrib.auth.views.password_reset',
        {'post_reset_redirect' : '/user/password/reset/done/'},
        name="password_reset"),
    url(r'^user/password/reset/done/$',
        'django.contrib.auth.views.password_reset_done'),
    url(r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect' : '/user/password/done/'}),
    url(r'^user/password/done/$',
        'django.contrib.auth.views.password_reset_complete'),
'''

