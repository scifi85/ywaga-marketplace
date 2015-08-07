from django.conf.urls.defaults import *
from cart.views import *

urlpatterns = patterns('',
    url(r'buy_product/(?P<product_id>\d+)/$',buy_product,name='buy_product'),
    url(r'product/(?P<product_id>\d+)/$',show,name='product'),
    url(r'cart/$',cart, name='cart'),
    url(r'change_number/(?P<cart_id>\d+)/(?P<quantity>\d+)/$',change_number),
    url(r'delete_cart/(?P<id>\d+)/$',delete_cart, name='delete_cart'),
    url(r'delete_order/(?P<id>\d+)/$',delete_order, name='delete_order'),
    url(r'cancel_order/(?P<id>\d+)/$',cancelOrder, name='cancel_order'),
    url(r'delete_address/(?P<id>\d+)/$',delete_address, name='delete_address'),
    url(r'orders/$',show_orders,name='orders'),
    url(r'pay/(?P<id>\d+)/$',pay, name='pay'),
    url(r'search_by_categories/(?P<categories>.*)/$',search_by_categories, name='category'),
    url(r'confirm_delivering/(?P<id>\d+)/$',confirm_delivering,name='confirm_delivering'),
#    url('^showshop/(?P<name>.*)/$',shop),
    url('^payments/$',payments,name='payments'),
    url('^make_payment/$',make_payment,name='make_payment'),

    url(r'^$', index, {'template':'public/first_page.html'},name='index'),
    url(r'^index/$', index, {'template':'public/firstPageA.html'},name='index'),
)