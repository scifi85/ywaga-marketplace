# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from statistic.models import *
from registr.models import RegistrationProfile
from cart.models import Order
from liqpay import *
from django.conf import settings
from shop.models import *

def showBalance(request):
    onAccounts=0.0
    for account in RegistrationProfile.objects.all():
        onAccounts+= account.account

    orders = Order.objects.all().exclude(status='Closed').exclude(status='Not payed')
    payed = 0.0
    for order in orders:
        if order.seller.get_profile().trustable:
            payed+=order.payed


    liq=Liqpay(settings.MERCHANT_ID,settings.SIGNATURE)
    usd=liq.get_ballances()
    usd=usd['USD']

    products = Product.objects.all().count()
    return render_to_response('statistic/balance.html',
            {'usd':usd,'balance':Balance.objects.show(),
             'onAccounts':onAccounts,'payed':payed,
             'products':products},
            context_instance=RequestContext(request))


