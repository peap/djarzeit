from django.conf.urls import url

from account import views


urlpatterns = [
    url(r'^$', views.account, name='account'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^new/$', views.new_account, name='new_account'),
]
