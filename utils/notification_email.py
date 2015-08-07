# -*- encoding: utf-8 -*-
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.template.loader import render_to_string


def sendEmail(user,type,extra=None):
    if type=='registr':
        password = extra[0]
        lang=user.get_profile().lang
        if lang=='ru':
            subject = 'Спасибо за регистрацию'
            text = render_to_string('emails/registration_ru.txt',{ 'user': user,'password':password})
        else:
            subject = 'Thank you for registration'
            text = render_to_string('emails/registration_en.txt',{ 'user': user,'password':password})

    if type=='track':
        lang=user.get_profile().lang
        seller = extra['seller']
        track_code = extra['track_code']
        order_id = extra['order_id']
        if lang=='ru':
            subject = 'Продавец %s обновил трекинг код' % seller
            text = render_to_string('emails/track_ru.txt',{ 'user': user,'track_code':track_code,'order_id':order_id})
        else:
            subject = 'Seller %s update tracking code' % seller
            text = render_to_string('emails/track_en.txt',{ 'user': user,'track_code':track_code,'order_id':order_id})

    if type=='buyerComplain':
        buyer=extra['buyer']
        cart=extra['cart']
        message = extra['message']
        refund=extra['refund']
        lang=user.get_profile().lang

        if lang=='ru':
            subject = 'Покупатель %s пожаловался' % buyer
            text = render_to_string('emails/buyerComplain_ru.txt',
                    { 'user': user,'cart':cart,'message':message,'refund':refund})
        else:
            subject = 'Buyer %s make complain' % buyer
            text = render_to_string('emails/buyerComplain_en.txt',
                    { 'user': user,'cart':cart,'message':message,'refund':refund})

    if type=='sellerComplain':
        seller=extra['seller']
        cart=extra['cart']
        message = extra['message']
        lang=user.get_profile().lang
        if lang=='ru':
            subject = 'Продавец %s ответил' % seller
            text = render_to_string('emails/sellerComplain_ru.txt',
                    { 'user': user,'cart':cart,'message':message})
        else:
            subject = 'Seller %s reply' % seller
            text = render_to_string('emails/sellerComplain_en.txt',
                    { 'user': user,'cart':cart,'message':message})
    if type=='InviteJudge':
        who = extra['who']
        cart = extra['cart']
        BorS = extra['BorS']
        lang=user.get_profile().lang
        if lang=='ru':
            subject = 'Пользователь %s пригласил судью' % who
            text = render_to_string('emails/inviteJudge_ru.txt',
                    { 'user': user,'cart':cart,'who':who,'BorS':BorS})
        else:
            subject = 'Seller %s invite judge' % who
            text = render_to_string('emails/inviteJudge_en.txt',
                    { 'user': user,'cart':cart,'who':who,'BorS':BorS})
    if type=='productFeedback':
        message = extra['message']
        product = extra['product']
        who = extra['who']

        lang=user.get_profile().lang
        if lang=='ru':
            subject = 'Пользователь %s оставил коментарий о вашем товаре' % who
            text = render_to_string('emails/productFeedback_ru.txt',
                    {'user': user,'who':who,'message':message,'product':product})
        else:
            subject = 'Customer %s left comment about your product' % who
            text = render_to_string('emails/productFeedback_en.txt',
                    {'user': user,'who':who,'message':message,'product':product})
    if type=='message':
        who = extra['from']
        message = extra['message']

        lang=user.get_profile().lang
        if lang=='ru':
            subject = 'Пользователь %s отправил вам сообщения' % who
            text = render_to_string('emails/new_message_ru.txt',
                    {'user': user,'who':who,'message':message})
        else:
            subject = 'User %s sent you message'%who
            text = render_to_string('emails/new_message_en.txt',
                    {'user': user,'who':who,'message':message})
    if type=='payedSeller':
        buyer = extra['buyer']
        order = extra['order']

        lang=user.get_profile().lang
        if lang=='ru':
            subject = 'Покупатеь %s оплатил заказ %s' % (buyer,order.id)
            text = render_to_string('emails/payedSeller_ru.txt',
                    {'user': user,'buyer': buyer,'order':order})
        else:
            subject = 'Customer %s payed for order %s'% (buyer,order.id)
            text = render_to_string('emails/payedSeller_en.txt',
                    {'user': user,'buyer': buyer,'order':order})

    if type=='payedBuyer':
        seller = extra['seller']
        order = extra['order']

        lang=user.get_profile().lang
        if lang=='ru':
            subject = 'Вы оплатили заказ %s' % order.id
            text = render_to_string('emails/payedBuyer_ru.txt',
                    {'user': user,'seller': seller,'order':order})
        else:
            subject = 'You payed for order %s'% order.id
            text = render_to_string('emails/payedBuyer_en.txt',
                    {'user': user,'seller': seller,'order':order})

    if type=='confirmSeller':
        buyer = extra['buyer']
        order = extra['order']

        lang=user.get_profile().lang
        if lang=='ru':
            subject = 'Покупатель %s подтверил доставку заказа %s' % (buyer,order.id)
            text = render_to_string('emails/confirmSeller_ru.txt',
                    {'user': user,'buyer': buyer,'order':order})
        else:
            subject = 'Buyer %s confirm delivering for order %s'% (buyer,order.id)
            text = render_to_string('emails/confirmSeller_en.txt',
                    {'user': user,'buyer': buyer,'order':order})

    if type=='confirmBuyer':
        seller = extra['seller']
        order = extra['order']

        lang=user.get_profile().lang
        if lang=='ru':
            subject = u'Вы подтвердили доставку заказа %s' % order.id
            text = render_to_string('emails/confirmBuyer_ru.txt',
                    {'user': user,'seller': seller,'order':order})
        else:
            subject = 'You confirm delivering for order %s'% order.id
            text = render_to_string('emails/confirmBuyer_en.txt',
                    {'user': user,'seller': seller,'order':order})
    if type=='TakeMoney':
        to = extra['to']
        amount = extra['amount']

        lang=user.get_profile().lang
        if lang=='ru':
            subject = u'Вы перевели %s$ на liqpay %s' % (amount,to)
            text = render_to_string('emails/TakeMoney_ru.txt',
                    {'user': user,'amount': amount,'to':to})
        else:
            subject = 'You send %s$ to liqpay account %s'% (amount,to)
            text = render_to_string('emails/TakeMoney_en.txt',
                    {'user': user,'amount': amount,'to':to})

    if type=='sendMoneyTo':
        to = extra['to']
        amount = extra['amount']

        lang=user.get_profile().lang
        if lang=='ru':
            subject = 'Вы перевели %s$ пользователю %s' % (amount,to)
            text = render_to_string('emails/TakeMoney_ru.txt',
                    {'user': user,'amount': amount,'to':to})
        else:
            subject = 'You send %s$ to ywaga account %s'% (amount,to)
            text = render_to_string('emails/TakeMoney_en.txt',
                    {'user': user,'amount': amount,'to':to})

    if type=='sendMoneyGet':
        fr = extra['from']
        amount = extra['amount']

        lang=user.get_profile().lang
        if lang=='ru':
            subject = 'Вы получили %s$ от пользователя %s' % (amount,fr)
            text = render_to_string('emails/sendMoneyGet_ru.txt',
                    {'user': user,'amount': amount,'from':fr})
        else:
            subject = 'You get %s$ from ywaga account %s'% (amount,fr)
            text = render_to_string('emails/sendMoneyGet_en.txt',
                    {'user': user,'amount': amount,'from':fr})

    if type=='getLiqpay':
        amount = extra['amount']

        lang=user.get_profile().lang
        if lang=='ru':
            subject = 'Вы получили %s$ через Liqpay' % amount
            text = render_to_string('emails/sendMoneyGet_ru.txt',
                    {'user': user,'amount': amount})
        else:
            subject = 'You get %s$ via Liqpay'% amount
            text = render_to_string('emails/sendMoneyGet_en.txt',
                    {'user': user,'amount': amount})
    if type=='cancelOrder':
        order = extra['order']

        lang=user.get_profile().lang
        if lang=='ru':
            subject = 'Заказ #%s отклонен' % order
            text = render_to_string('emails/sendMoneyGet_ru.txt',
                    {'user': user,'order': order})
        else:
            subject = 'Order #%s is canceled'% order
            text = render_to_string('emails/sendMoneyGet_en.txt',
                    {'user': user,'order': order})
    if type=='complainCloseBuyer':
        complain= extra['complain']

        lang=user.get_profile().lang
        if lang=='ru':
            subject = 'Жалоба #%s от %s удовлетворена' % (complain.id, complain.buyer)
            text = render_to_string('emails/complainCloseBuyer_ru.txt',
                    {'user': user,'complain': complain})
        else:
            subject = 'Complain #%s from %s is satisfied'% (complain.id, complain.buyer)
            text = render_to_string('emails/complainCloseBuyer_en.txt',
                    {'user': user,'complain': complain})

    if type=='complainCloseSeller':
        complain= extra['complain']
        lang=user.get_profile().lang
        if lang=='ru':
            subject = 'Жалоба #%s от %s не удовлетворена' % (complain.id, complain.buyer)
            text = render_to_string('emails/complainCloseSeller_ru.txt',
                    {'user': user,'complain': complain})
        else:
            subject = 'Complain #%s from %s is not satisfied'% (complain.id, complain.buyer)
            text = render_to_string('emails/complainCloseSeller_en.txt',
                    {'user': user,'complain': complain})
    if type=='createOrder':
        order = extra['order']
        lang=user.get_profile().lang
        if lang=='ru':
            subject = 'Поступил заказ #%s от пользователя %s'%(order.id,order.buyer)
            text = render_to_string('emails/createOrder_ru.txt',
                                    {'user': user,'order': order})
        else:
            subject = 'Receive order #%s from user %s'% (order.id, order.buyer)
            text = render_to_string('emails/createOrder_en.txt',
                                    {'user': user,'order': order})


#    return 1
    return send_mail(subject,text,'no_reply@ywaga.com',[user.email,],fail_silently=True)
