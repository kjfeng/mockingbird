from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'survey_complete', views.survey_complete, name='survey_complete'),
    url(r'', views.survey, name='survey'),
]
