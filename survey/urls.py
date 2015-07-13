from django.conf.urls import patterns, url
from django.conf.urls.defaults import include
from django.conf.urls.static import static
from django.conf import settings

from survey import survey_views

urlpatterns = patterns('',
    url(r'^$', survey_views.main_page, name='index'),
    url(r'^(?P<survey_pk>\d+)/(?P<page_num>\d+)/questions/$', survey_views.question_page, name='questiondetail'),
    url(r'^(?P<survey_pk>\d+)/(?P<page_num>\d+)/response/$', survey_views.response, name='response'),
    url(r'^(?P<survey_pk>\d+)/(?P<page_num>\d+)/back/$', survey_views.back, name='back'),
    url(r'^(?P<survey_pk>\d+)/completed/$', survey_views.completed, name='completed'),
    url(r'^(?P<survey_pk>\d+)/save/$', survey_views.save_survey, name='save_survey'),
    url(r'^(?P<survey_pk>\d+)/notavailable/$', survey_views.survey_not_available, name='notavailable'),
)# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
