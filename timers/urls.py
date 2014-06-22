from django.conf.urls import patterns, include, url

from timers import views

timer_patterns = patterns('',
    url(r'^startstop/$', views.StartStop.as_view(), name='startstop'),
    url(r'^edit/$', views.edit_timer, name='edit_timer'),
    url(r'^archive/$', views.archive_timer, name='archive_timer'),
    url(r'^unarchive/$', views.unarchive_timer, name='unarchive_timer'),
    url(r'^delete/$', views.delete_timer, name='delete_timer'),
)

urlpatterns = patterns('',
    url(r'^$', views.TimersListing.as_view(), name='timers'),
    url(r'^new/(?P<category_id>[0-9]{1,20})/$',
        views.NewTimer.as_view(),
        name='new_timer'),
    url(r'^(?P<timer_id>[0-9]{1,20})/', include(timer_patterns)),
)
