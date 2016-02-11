from django.conf.urls import include, url

from timers import views


class SingleTimerPatterns():
    urlpatterns = [
        url(r'^startstop/$', views.StartStop.as_view(), name='startstop'),
        url(r'^edit/$', views.Edit.as_view(), name='edit_timer'),
        url(r'^archive/$', views.Archive.as_view(), name='archive_timer'),
        url(r'^unarchive/$', views.Archive.as_view(), name='unarchive_timer'),
        url(r'^delete/$', views.Delete.as_view(), name='delete_timer'),
    ]


urlpatterns = [
    url(r'^$', views.Listing.as_view(), name='timers'),
    url(r'^new/(?P<category_id>[0-9]{1,20})/$', views.New.as_view(), name='new_timer'),
    url(r'^(?P<timer_id>[0-9]{1,20})/', include(SingleTimerPatterns)),
    url(r'^timeline/$', views.Timeline.as_view(), name='timeline'),
]
