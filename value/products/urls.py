from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.products.views',
    url(r'^$', 'products', name='products'),
    url(r'^(\d+)/$', 'product', name='product'),
)
