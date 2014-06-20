from django.conf.urls import patterns, include, url

import account.urls
import categories.urls
import timers.urls
import reports.urls

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'account.views.login', name='home'),

    url(r'^account/', include(account.urls)),
    url(r'^categories/', include(categories.urls)),
    url(r'^timers/', include(timers.urls)),
    url(r'^reports/', include(reports.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
