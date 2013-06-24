from django.conf.urls import patterns, include, url

from tags import views

tag_patterns = patterns('',
    url(r'^$', views.tag, name='tag'),
    url(r'^delete/$', views.delete_tag, name='delete_tag'),
)

urlpatterns = patterns('',
    url(r'^$', views.tags, name='tags'),
    url(r'^new/$', views.new_tag, name='new_tag'),
    url(r'^(?P<id>[0-9]{1,20})/', include(tag_patterns)),
)
