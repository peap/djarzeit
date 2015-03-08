from django.conf.urls import patterns, url

from reports import views


urlpatterns = patterns('',
    url(r'^intervals/day/$', views.intervals, name='intervals'),

    url(r'^day/$', views.daily_summary, name='daily_summary'),
    url(r'^day/full/$',views.daily_summary, {'full': True}, name='daily_summary_full'),

    url(r'^week/$', views.weekly_summary, name='weekly_summary'),
    url(r'^week/full/$', views.weekly_summary, {'full': True}, name='weekly_summary_full'),
)
