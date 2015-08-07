# -*- encoding: utf-8 -*-
from liqpay import *
from payments.models import Payment
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect
from payments.models import Payment
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse
from paypal.standard.ipn.signals import payment_was_successful,payment_was_flagged
from log.models import *
from notification_email import sendEmail
from statistic.models import Balance
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

@csrf_exempt
@require_POST
def get_liqpay(request):
    user=User.objects.get(id=1)
    SystemLog.objects.create(user=user, type='payment', text='GET LIQPAY')

    liq=Liqpay(settings.MERCHANT_ID,settings.SIGNATURE)
    response=liq.parse_merchant_response_xml(opxml=request.POST['operation_xml'],signature=request.POST['signature'])
    username = request.GET['username']
    user = User.objects.get(username=username)

    if (response.status=='success'):
        Payment.objects.create(status = response.status,pay_way = 'liqpay',
            sender_phone = response.sender_phone,
            code = response.code,
            amount = response.amount,
            currency = response.currency,
            description = response.description,
            pay_details = response.pay_details,
            type='in',
            invoice_id = response.order_id,
            user=user
        )
        user.get_profile().account+=float(response.amount)
        user.get_profile().save()

        UserLog.objects.create(user=user, type='payment',
            text_en='You add %s$ to own account by liqpay' % float(response.amount),
            text_ru=u'Вы поставили %s$ на свой счет с помощью liqpay' % float(response.amount)
        )
        sendEmail(user=user,type='getLiqpay',extra={'amount':amount})
        SystemLog.objects.create(user=user, type='payment', text='User %s add %s$  to account by liqpay'% (user.username,response.amount))
        Balance.objects.addToBalance(response.amount)
    else:
        UserLog.objects.create(user=user, type='payment',
            text_en='Failed to add %s$ to own account by liqpay' % response.amount,
            text_ru=u'Liqpay транзакция на суму %s$ не прошла обратитесь в службу поддержки ликпей на liqay.com' % response.amount
        )

    return HttpResponse('complete')

def show_me_the_money(sender, **kwargs):
    if sender.payment_status=='Completed':
        try:
            user = User.objects.get(username=sender.item_name)
        except :
            user = User.objects.get(username='buyer')
        Payment.objects.create(status = 'success',pay_way = 'paypal',
            amount = sender.mc_gross,
            currency = sender.mc_currency,
            paypal=sender.txn_id,
            type='in',
            user=user
        )
        Balance.objects.addToBalance(sender.mc_gross)
        profile=user.get_profile()
        profile.account+=float(sender.mc_gross)
        profile.save()
        UserLog.objects.create(user=user, type='payment',
                text_en='You add %s$ to own account by paypal' % sender.mc_gross,
                text_ru=u'Вы поставили %s$ на свой счет с помощью paypal' % sender.mc_gross
            )
        SystemLog.objects.create(user=user, type='payment', text='User %s add to account %s$ by paypal'% (user.username,sender.mc_currency))
    else:
        UserLog.objects.create(user=user, type='payment',
            text_en='Paypal transaction on amount %s$ was failed' % sender.mc_currency,
            text_ru=u'Paypal транзакция на суму %s$ отменена' % sender.mc_currency
        )



payment_was_successful.connect(show_me_the_money)
payment_was_flagged.connect(show_me_the_money)


def send_money(request):
    try:
        amount = float(request.POST['amount'])

        if amount>request.user.get_profile().account:
            messages.error(request,'Not enough money')
            return HttpResponseRedirect(reverse('payments'))

        user = User.objects.get(username=request.POST['username'])
        if user==request.user:
            messages.error(request,'Can not send money to yourself')
            return HttpResponseRedirect(reverse('payments'))
        user.get_profile().account += amount
        user.get_profile().save()
        request.user.get_profile().account -= amount
        request.user.get_profile().save()
        messages.success(request,'Payment successful')
        UserLog.objects.create(user=request.user, type='payment',
            text_en='Sent %s$ to user %s' % (amount,user.username),
            text_ru=u'Выслано %s$ пользователю %s' % (amount,user.username))
        UserLog.objects.create(user=user, type='payment',
            text_en='Get money %s$ from %s' % (amount,request.user.username),
            text_ru=u'Получено %s$ от %s' % (amount,request.user.username)
        )

        sendEmail(user=request.user, type='sendMoneyTo',extra={'to':user,'amount':amount})
        sendEmail(user=user, type='sendMoneyGet',extra={'from':request.user,'amount':amount})


        SystemLog.objects.create(user=request.user, type='payment', text='Send %s to user %s' % (amount,user.username))
    except :
        messages.error(request,'Error')

    return HttpResponseRedirect(reverse('payments'))

@require_POST
def take_money(request):
    liq=Liqpay(settings.MERCHANT_ID,settings.SEND_MONEY_SIGNATURE)
    amount=float(request.POST['amount'])
    if amount>request.user.get_profile().account or amount==0:
        messages.error(request,_(u'Не достаточно денег на вашем счету'))
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    to=request.POST['to']
    comission=amount/100*float(settings.COMISSION_RATE)
    try:
        liq.send_money(to=to,amount=amount-comission,currency='USD')
        liq.send_money(to=settings.COMISSION_PHONE,amount=comission,currency='USD')

        UserLog.objects.create(user=request.user, type='payment',
            text_ru=u'Выведено %s$ на liqpay счет %s ' % (amount,to),
            text_en='Sent %s$ to liqpay account %s ' % (amount,to),
        )
        SystemLog.objects.create(user=request.user, type='payment',
            text='Sent %s$ to liqpay account %s ' % (amount,to))

        Balance.objects.outFromBalance(amount)
        Balance.objects.commission(comission)

        profile = request.user.get_profile()
        profile.account-=amount
        profile.save()

        sendEmail(user=request.user, type='TakeMoney',extra={'to':to,'amount':amount})
    except Exception, err:
        messages.error(request,err)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])