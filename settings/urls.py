from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'edit_settings', views.edit_settings, name='edit_settings'),
    url(r'', views.settings, name='settings'),

]