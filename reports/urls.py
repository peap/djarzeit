from django.conf.urls import patterns, include, url

from reports import views


urlpatterns = patterns('',
    url(r'^$', views.reports, name='reports'),
    url(r'^day/$', views.daily_summary, name='daily_summary'),
    url(r'^week/$', views.weekly_summary, name='weekly_summary'),
    url(r'^intervals/$', views.intervals, name='intervals'),
)
