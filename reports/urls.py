from django.conf.urls import patterns, include, url

from reports import views


urlpatterns = patterns('',
    url(r'^day/$', views.daily_summary, name='daily_summary'),
    url(r'^week/$', views.weekly_summary, name='weekly_summary'),
    url(r'^week_by_day/$', views.weekly_by_day, name='weekly_by_day'),
    url(r'^intervals/$', views.intervals, name='intervals'),
)
