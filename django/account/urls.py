from django.conf.urls import url
from . import views
from onboard import views as onboard_views

app_name = 'account'
urlpatterns = [
    url(r'^confirm_delete/$', views.account_delete_confirm, name='confirm_delete'),
    url(r'^delete/$', views.account_delete, name='delete'),
    url(r'^edit/$', views.account_edit, name='edit'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^statistics/$', views.show_statistics, name='show_statistics'),
    url(r'^(?P<username>\w+)/$', views.profile_view, name='profile_view'),
    url(r'', views.account_details, name='account_details'),
]
