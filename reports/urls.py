from django.conf.urls import url

from reports.views import daily_summary, intervals, totals, weekly_summary


urlpatterns = [
    url(r'^intervals/day/$', intervals, name='intervals'),

    url(r'^day/$', daily_summary, name='daily_summary'),
    url(r'^day/full/$', daily_summary, {'full': True}, name='daily_summary_full'),

    url(r'^week/$', weekly_summary, name='weekly_summary'),
    url(r'^week/full/$', weekly_summary, {'full': True}, name='weekly_summary_full'),

    url(r'^totals/$', totals, name='totals_between_dates'),
]
