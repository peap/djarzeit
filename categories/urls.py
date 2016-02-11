from django.conf.urls import include, url

from categories import views


class SingleCategoryPatterns():
    urlpatterns = [
        url(r'^$', views.category, name='category'),
        url(r'^new/$', views.new_category, name='new_category'),
        url(r'^delete/$', views.delete_category, name='delete_category'),
    ]

urlpatterns = [
    url(r'^$', views.categories, name='categories'),
    url(r'^(?P<cat_id>([0-9]{1,20}|root))/', include(SingleCategoryPatterns)),
]
