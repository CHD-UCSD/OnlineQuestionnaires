from django.conf.urls import patterns, include, url
from django.conf import settings
#from django_consultants.views import *
#from django.conf.urls.defaults import *
from surveysite import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'survey.survey_views.main_page'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^survey/', include('survey.urls', namespace='survey')),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', views.logout_page),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset'),
    url(r'^password_reset_done/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^password_reset_confirm/$', 'django.contrib.auth.views.password_reset_confirm'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'post_reset_redirect': '/logout/' }),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
