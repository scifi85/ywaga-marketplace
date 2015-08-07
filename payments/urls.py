from django.conf.urls.defaults import *
from payments.views import get_liqpay,send_money,take_money

urlpatterns = patterns('',
    url(r'paypal/dsfwelko/$', include('paypal.standard.ipn.urls')),
    url(r'get_liqpay/$', get_liqpay),
    url(r'send_money/$', send_money,name='send_money'),
    url(r'take_money/$', take_money,name='take_money'),

)


