from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'timers.views.home', name='home'),
    url(r'^new/$', 'timers.views.new', name='new'),
    url(r'^(?P<id>[0-9]{1,20})/$', 'timers.views.timer', name='timer'),
    url(r'^(?P<id>[0-9]{1,20})/startstop/$', 'timers.views.startstop', name='startstop'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
