from django.conf.urls import patterns, include, url

from timers import views

timer_patterns = patterns('',
    url(r'^edit/$', views.edit_timer, name='edit_timer'),
    url(r'^delete/$', views.delete_timer, name='delete_timer'),
    url(r'^startstop/$', views.startstop, name='startstop'),
)

urlpatterns = patterns('',
    url(r'^$', views.timers, name='timers'),
    url(r'^new/$', views.new_timer, name='new_timer'),
    url(r'^(?P<timer_id>[0-9]{1,20})/', include(timer_patterns)),
)
