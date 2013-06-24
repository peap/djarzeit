from django.conf.urls import patterns, include, url

import account.urls

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'timers.views.home', name='home'),

    url(r'^categories/new/$', 'timers.views.new_category', name='new_category'),
    url(r'^categories/(?P<id>[0-9]{1,20})/$', 'timers.views.category', name='category'),
    url(r'^categories/(?P<id>[0-9]{1,20})/delete/$', 'timers.views.delete_category', name='delete_category'),

    url(r'^timers/new/$', 'timers.views.new_timer', name='new_timer'),
    url(r'^timers/(?P<id>[0-9]{1,20})/$', 'timers.views.timer', name='timer'),
    url(r'^timers/(?P<id>[0-9]{1,20})/delete/$', 'timers.views.delete_timer', name='delete_timer'),
    url(r'^timers/(?P<id>[0-9]{1,20})/startstop/$', 'timers.views.startstop', name='startstop'),

    url(r'^account/', include(account.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
