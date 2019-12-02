from django.conf.urls import url
from . import views

app_name = 'account'
urlpatterns = [
    url(r'^delete/$', views.account_delete, name='delete'),
    url(r'^edit/$', views.account_edit, name='edit'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'', views.account_details, name='account_details')
]
