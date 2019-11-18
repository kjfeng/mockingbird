from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^delete/$', views.account_delete, name='delete'),
    url(r'^edit/$', views.account_edit, name='edit'),
    url(r'', views.account_details, name='account_details'),
    url(r'^change-password/$', views.change_password, name='change_password'),
]