from django.conf.urls.defaults import *
from shop.views import *
urlpatterns = patterns('',
    url(r'delete_product/(?P<product_id>\d+)/$',delete_product,name='delete_product'),
    url(r'add_product/$',add_product,{'product_id':None},name='add_product'),
    url(r'addProductFromTB/$',addProductFromTB,name='addProductFromTB'),
    url(r'orders/$', show_shop_orders,name='show_my_orders'),
    url(r'edit_product/(?P<product_id>\d+)/$',add_product,name='edit_product'),
    url(r'get_categories/$',get_categories, ({'categories':None}),name='get_categories'),
    url(r'get_categories/(.*)/$',get_categories,name='get_category'),
    url(r'capture_tmp/$',capture_tmp),
    url(r'^$', show_products, name='show'),
    url(r'change/(?P<cart_id>\d+)/(?P<value>\d+|\d+.\d+|\w+)/(?P<type>\w+)/$', change, name='change'),
    url(r'upload_track_code/(?P<order_id>\d+)/', upload_track_code,name='upload_track_code'),
    url(r'contacts/$',contacts,name='contact'),
    url(r'action/',action,name='action'),
#    url(r'setTrust/(?P<trust>\w+)/$',setTrust,name='setTrust')

)