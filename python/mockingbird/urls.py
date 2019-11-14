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
    path('tags/', tags_views.tags_view),
    path('', match_views.match_view, name='home'),
    path('match/', match_views.match_view),
    path('matchresults/', match_views.matchresults_view),
    url(r'^signup/$', onboard_views.signup, name='signup'),
    url(r'^account_activation_sent/$', onboard_views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        onboard_views.activate, name='activate'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^account/', include(('account.urls','account'), namespace='account')),
]
