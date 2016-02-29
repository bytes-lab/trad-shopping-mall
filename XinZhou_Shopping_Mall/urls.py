from django.conf.urls import patterns, include, url
# from shopping_mall.adminsite import Shopping_Mall_Admin
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^polls/', include('polls.urls', namespace="polls")),
                       url(r'^shopping_mall/', include('shopping_mall.urls', namespace="shopping_mall")),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^image_upload/(?P<product_id>\d+)/$', 'shopping_mall.views.image_upload', ),
                       url(r'^image_spec/(?P<product_id>\d+)/$', 'shopping_mall.views.image_spec', )
                       )
