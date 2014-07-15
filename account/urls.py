from django.conf.urls import patterns, url

from account import views


urlpatterns = patterns('',
    url(r'^$', views.account, name='account'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^new/$', views.new_account, name='new_account'),
)
