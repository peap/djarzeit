from django.conf.urls import patterns, include, url

from categories import views

category_patterns = patterns('',
    url(r'^/$', views.category, name='category'),
    url(r'^delete/$', views.delete_category, name='delete_category'),
)

urlpatterns = patterns('',
    url(r'^/$', views.categories, name='categories'),
    url(r'^new/$', views.new_category, name='new_category'),
    url(r'^(?P<id>[0-9]{1,20})/', include(category_patterns),
)
