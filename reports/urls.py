from django.conf.urls import patterns, url

from reports import views


urlpatterns = patterns('',
    url(r'^day/$', views.daily_summary, name='daily_summary'),
    url(r'^week/$', views.weekly_summary, name='weekly_summary'),
    url(r'^intervals/$', views.intervals, name='intervals'),
)
