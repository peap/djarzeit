from django.conf.urls import patterns, include, url

import account.urls
import categories.urls
import timers.urls
import reports.urls


urlpatterns = patterns('',
    url(r'^$', 'account.views.login', name='home'),
    url(r'^account/', include(account.urls)),
    url(r'^categories/', include(categories.urls)),
    url(r'^timers/', include(timers.urls)),
    url(r'^reports/', include(reports.urls)),
)
