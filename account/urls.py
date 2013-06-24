from django.conf.urls import patterns, include, url

from account import views

urlpatterns = patterns('',
    url(r'^$', views.account, name='account'),
    url(r'^login/$', views.login, name='login'),
    url(r'^new/$', views.new_account, name='new_account'),
)
