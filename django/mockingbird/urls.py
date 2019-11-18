<<<<<<< HEAD:django/mockingbird/urls.py
=======
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
>>>>>>> eb74751bd8d40917df3d6889786701ef058c0e27:python/mockingbird/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views

from django.conf.urls import url
from onboard import views as onboard_views
<<<<<<< HEAD:django/mockingbird/urls.py
from match import views as match_views
from tags import views as tags_views
=======
>>>>>>> eb74751bd8d40917df3d6889786701ef058c0e27:python/mockingbird/urls.py

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
<<<<<<< HEAD:django/mockingbird/urls.py
    path('tags/', tags_views.tags_view),
    path('', match_views.match_view, name='home'),
    path('match/', match_views.match_view),
    path('matchresults/', match_views.matchresults_view),
    url(r'^signup/$', onboard_views.signup, name='signup'),
=======
    path('', onboard_views.login, name='home'),
    url(r'^signup/$', onboard_views.signup, name='signup'),
    url(r'^login/$', onboard_views.login, name='login'),
     url(r'^ForgotPassword/$', onboard_views.forgotPassword, name='forgotPassword'),
>>>>>>> eb74751bd8d40917df3d6889786701ef058c0e27:python/mockingbird/urls.py
    url(r'^account_activation_sent/$', onboard_views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        onboard_views.activate, name='activate'),
    url('^', include('django.contrib.auth.urls')),
<<<<<<< HEAD:django/mockingbird/urls.py
    url(r'^account/', include(('account.urls','account'), namespace='account')),
]
=======
]
>>>>>>> eb74751bd8d40917df3d6889786701ef058c0e27:python/mockingbird/urls.py
