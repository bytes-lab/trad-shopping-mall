from django.conf.urls import patterns, url
from shopping_mall import views

urlpatterns = patterns('',
                       url(r'^product_category', views.product_category, name='product_category'),
                       url(r'^product_all', views.get_product_all, name='product_all'),
                       url(r'^get_brand_select', views.get_brands, name='brand_select'),
                       url(r'^spec_products/(?P<page_type>\d+)/$', views.spec_products, name='spec_products'),
                       )
