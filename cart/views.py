# -*- encoding: utf-8 -*-
from registr.forms import RegistrationFormUniqueEmail,LoginForm
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.contrib.auth.decorators import login_required
from cart.models import *
from shop.models import *
import simplejson
from cart.forms import *
from django.contrib import messages
from datetime import *
from log.models import *
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import random
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.translation import ugettext_lazy as _
from liqpay import *
from news.models import *
from notification_email import sendEmail
from django.conf import settings

def search_by_categories(request,categories):
    categories = re.findall('\d+',categories)

    products = Product.objects.search_by_categories(categories)
    products=Paginator(products,25)
    try:
        page = request.GET['page']
    except:
        page = 1

    try:
        products = products.page(page)
    except (EmptyPage, InvalidPage):
        products = products.page(products.num_pages)
    view=None
    if 'view' in request.GET:
        if request.GET['view']=='extend':
            view='extend'
    return render_to_response('public/categories.html',{'products':products,'categories':categories,'view':view},context_instance=RequestContext(request))

@csrf_exempt
def index(request,template):
    view=None
    if request.subdomain:
        products= Product.objects.filter(is_active=True, is_deleted=False,user__username=request.subdomain)
        shop=products.all()[0].user
        products=Paginator(products,25)
        try:
            page = request.GET['page']
        except:
            page = 1

        try:
            products = products.page(page)
        except (EmptyPage, InvalidPage):
            products = products.page(products.num_pages)
        if 'view' in request.GET:
            if request.GET['view']=='extend':
                view='extend'

        return render_to_response('public/shop.html',{'products':products,'view':view,'shop':shop},context_instance=RequestContext(request))

    if 'q' in request.GET:
        query=request.GET['q']
        if query=='':
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        products = Product.objects.active().search(query)

        products=Paginator(products,25)
        try:
            page = request.GET['page']
        except:
            page = 1

        try:
            products = products.page(page)
        except (EmptyPage, InvalidPage):
            products = products.page(products.num_pages)

    else:
        try:
            lastNews=NewsItem.objects.all()[0] or ''
            products = Product.objects.filter(is_active=True, is_deleted=False).exclude(picture='nopic.png')
            products = list(products[:100])
            random.shuffle(products)
            products = products[:10]
        except :
            lastNews=''

        return render_to_response(template,{'lastNews':lastNews,'newProducts':products},context_instance=RequestContext(request))

    if 'view' in request.GET:
        if request.GET['view']=='extend':
            view='extend'
    return render_to_response('public/search.html',{'products':products,'view':view,'query':query},context_instance=RequestContext(request))

def show(request,product_id):
    product = get_object_or_404(Product,id=product_id,is_active=True, is_deleted=False )
    is_allowed_comment = product.is_allowed_comment(request.user)
    comments = product.comments.all()
    comments=Paginator(comments,5)
    try:
        page = request.GET['page']
    except:
        page = 1

    try:
        comments = comments.page(page)
    except (EmptyPage, InvalidPage):
        comments = comments.page(comments.num_pages)
    return render_to_response('public/show.html',{'comments':comments,'product':product,'is_allowed_comment':is_allowed_comment},context_instance=RequestContext(request))

@login_required
def show_orders(request):
    payed_orders = request.user.get_profile().payed().exclude(status='Closed')
    not_payed_orders = request.user.get_profile().not_payed().exclude(status='Closed')
    closed_orders=request.user.get_profile().allOrders().filter(status='Closed')

    payed_orders=Paginator(payed_orders,10)
    try:
        page = request.GET['page2']
    except:
        page = 1
    try:
        payed_orders = payed_orders.page(page)
    except (EmptyPage, InvalidPage):
        payed_orders = payed_orders.page(payed_orders.num_pages)

    not_payed_orders=Paginator(not_payed_orders,10)
    try:
        page2 = request.GET['page']
    except:
        page2 = 1
    try:
        not_payed_orders = not_payed_orders.page(page2)
    except (EmptyPage, InvalidPage):
        not_payed_orders = not_payed_orders.page(not_payed_orders.num_pages)

    closed_orders=Paginator(closed_orders,10)
    try:
        page3 = request.GET['page3']
    except:
        page3 = 1
    try:
        closed_orders = closed_orders.page(page3)
    except (EmptyPage, InvalidPage):
        closed_orders = closed_orders.page(closed_orders.num_pages)


    return render_to_response('cart/orders.html',{'payed_orders':payed_orders,'not_payed_orders':not_payed_orders,'closed_orders':closed_orders}, context_instance=RequestContext(request))

#def shop(request,name):
#    products= Product.objects.filter(is_active=True, is_deleted=False,user__username=name)
#    return render_to_response('public/shop.html',{'products':products},context_instance=RequestContext(request))


def buy_product(request,product_id):
    product = Product.objects.get(id=product_id)
    carts=CartItem.objects.filter(cart_id=request.session['cart_id'])
    if request.user==product.user:
        messages.error(request,_(u'Вы не можете купить свой товар'))
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    try:
        quantity = int(request.POST['quantity'])
    except :
        quantity=1

    if quantity>product.quantity:
        messages.info(request,_(u'Не достаточно товара, уменьшите количество'))
#        messages.info(request,'not enough product, decrease quantity')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    try:
        color = int(request.POST['color'])
        color = Colors.objects.get(id=color)
        color_price = color.price
    except :
        color_price,color=-1,None

    try:
        size = int(request.POST['size'])
        size = Sizes.objects.get(id=size)
        size_price = size.price
    except :
        size_price,size =-1,None

    try:
        type = int(request.POST['type'])
        type= Types.objects.get(id=type)
        type_price = type.price
    except :
        type_price,type=-1,None

    price = max(color_price,size_price,type_price)
    if price==-1:
        price=product.price
#    product_price=product.price if not product.is_promotion else product.promotion_price
#    price = product_price if price==-1 else price
    if product.is_promotion:
        price=product.promotion_price

    product_in_cart = False
    for item in carts:
        if item.product==product and item.price==price and item.color==color and item.size==size and item.type==type:
            item.quantity+= quantity
            item.save()
            product_in_cart=True

    if not product_in_cart:

        delivery=0 if product.is_external else product.external_delivery
        CartItem.objects.create(cart_id=request.session['cart_id'],product=product,
            color = color, size = size, type = type,delivery = delivery,
            quantity=quantity, price=price)

    messages.success(request,_(u"Товар добавлен в корзину <br><br> <a href='/cart/' class='cartyes'>Перейти в корзину</a> &rarr;"))
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
#    return HttpResponseRedirect(reverse('cart'))

def cart(request):
    carts=CartItem.objects.filter(cart_id=request.session['cart_id'])
    full_price = carts.full_price()
    carts=carts.order_by_shop()

    if request.user.is_authenticated():
        lForm,rForm='',''
    else:
        lForm,rForm=LoginForm(),RegistrationFormUniqueEmail()

    addressForm = AddressForm()

    if request.method == 'POST':
        address= request.POST['address'] if 'address' in request.POST else 'new'
        addressForm = AddressForm(request.POST)
        lForm = LoginForm(request.POST)
        if not addressForm.is_valid()  and address=='new':
            if not request.user.is_authenticated():
                return render_to_response('public/cart.html',{'carts':carts,'full_price':full_price, 'rForm':rForm,'lForm':lForm,'addressForm':addressForm},context_instance=RequestContext(request))
            else:
                return render_to_response('cart/cart.html',{'carts':carts,'full_price':full_price, 'rForm':rForm,'lForm':lForm,'addressForm':addressForm},context_instance=RequestContext(request))
#            messages.info(request,'Enter address')
#            return HttpResponseRedirect(reverse('cart'))

        if lForm.is_valid():
            user = authenticate(username=lForm.cleaned_data['login'], password=lForm.cleaned_data['password'])
            #if user try to login by email in username
            if user is None:
                username=User.objects.filter(email=lForm.cleaned_data['login'])
                if username:
                    username=username[0].username
                    user = authenticate(username=username, password=lForm.cleaned_data['password'])
                else:
                    from django.forms.forms import NON_FIELD_ERRORS
                    lForm._errors[NON_FIELD_ERRORS] = lForm.error_class(["Your username or password was incorrect."])

            if user is not None and user.is_active:
                for shop in carts:
                    for cart in shop.carts.all():
                        if cart.product.user==user:
                            messages.error(request,_(u'Вы не можете купить товар у самого себя'))
                            return render_to_response('public/cart.html',{'carts':carts,'full_price':full_price, 'rForm':rForm,'lForm':lForm,'addressForm':addressForm},context_instance=RequestContext(request))
                login(request,user)

        rForm= RegistrationFormUniqueEmail(request.POST)
        if rForm.is_valid():
            rForm.save()
            user = authenticate(username=rForm.cleaned_data['username'], password=rForm.cleaned_data['password1'])
            login(request,user)

        if  rForm.is_valid() or lForm.is_valid() or request.user.is_authenticated():
            if address=='new':
                address = addressForm.save()
                request.user.get_profile().addresses.add(address)
            else:
                address=address.replace('address_','')
                address=request.user.get_profile().addresses.get(id=address)

            shops=CartItem.objects.filter(cart_id=request.session['cart_id']).order_by_shop()

            for shop in shops:
                order=Order.objects.create(seller=shop.user,buyer = request.user,
                    status = 'Not payed', country = address.country,
                    region = address.region, phone = address.phone,
                    city = address.city,street = address.street, zip_code = address.zip_code)
                for cart in shop.carts:
                    cart.cart_id=''
                    cart.save()
                    order.carts.add(cart)
                request.user.get_profile().orders.add(order)

                UserLog.objects.create(user=order.seller,
                    text_en=(u'Got <a href="/shop/orders/">  order #%s</a> from user %s'% (order.id,order.buyer)),
                    text_ru=(u'Поступил <a href="/shop/orders/"> заказ #%s</a> от пользователя %s'% (order.id,order.buyer)))
                UserLog.objects.create(user=order.buyer,
                    text_en=(u'Created <a href="/orders/">order #%s</a>' % order.id),
                    text_ru=(u'Создан <a href="/orders/">заказ #%s</a>' % order.id))
                SystemLog.objects.create(user=request.user,text='Create order %s' % order.id)
                sendEmail(user=order.seller,type='createOrder',extra={'order':order})
            messages.success(request,u'Спасибо за заказ! Продавец свяжется с вами в кратчайшие сроки.')
            return HttpResponseRedirect(reverse('orders'))

    if not request.user.is_authenticated():
        return render_to_response('public/cart.html',{'carts':carts,'full_price':full_price, 'rForm':rForm,'lForm':lForm,'addressForm':addressForm},context_instance=RequestContext(request))

    return render_to_response('cart/cart.html',{'carts':carts,'full_price':full_price, 'rForm':rForm,'lForm':lForm,'addressForm':addressForm},context_instance=RequestContext(request))

def change_number(request,cart_id,quantity):
    try:
        whole_cart = CartItem.objects.filter(cart_id=request.session['cart_id'])
        cart=whole_cart.get(id=cart_id)
        quantity=int(quantity)
        if quantity>cart.product.quantity:
            resp={'max':cart.product.quantity,'q':cart.quantity}
            return HttpResponse(simplejson.dumps(resp))
        cart.quantity =quantity
        cart.save()

        price = cart.full_price()
        sum = whole_cart.full_price()
        shop_price = whole_cart.filter(product__user=cart.product.user).full_price()

        resp = {'price':str(price),'sum':str(sum), 'shop_price':str(shop_price)}
        if request.user.is_authenticated():
            SystemLog.objects.create(user=request.user,text='For cart %s, product id=%s, name=%s, changed quantity to %s' %
                (cart.id,cart.product.id,cart.product.name,quantity))
    except :

        resp = 'error'

    return HttpResponse(simplejson.dumps(resp))

def delete_cart(request,id):
    cart = get_object_or_404(CartItem,id=id)
    userCart =  CartItem.objects.filter(cart_id=request.session['cart_id'])
    if request.user.is_authenticated():
        inOrder = request.user.get_profile().orders.filter(carts=cart, is_payed=False) or \
            Order.objects.filter(seller=request.user, carts=cart,is_payed=False)
        if cart in userCart or inOrder:
            SystemLog.objects.create(user=request.user,text='cart %s, deleted' % cart.id)
            if cart.order():
                UserLog.objects.create(user=cart.order().buyer,
                    text_ru=u'Продавец %s удалил товар %s'%(cart.order().seller,cart.product.name),
                    text_en='Seller %s removed order %s'%(cart.order().seller,cart.product.name))
                UserLog.objects.create(user=cart.order().seller,
                    text_ru=u'Вы удалили товар %s'%cart.product.name,
                    text_en='You removed order %s'%cart.product.name)
            cart.delete()


        for order in inOrder:
            if order.carts.all().count()==0 and order.is_payed==False:
                UserLog.objects.create(user=order.buyer,
                    text_ru=u'Продавец %s удалил заказ #%s'%(order.seller,order.id),
                    text_en='Seller %s removed order #%s'%(order.seller,order.id))
                UserLog.objects.create(user=order.seller,
                    text_ru=u'Вы удалили заказ #%s'%order.id,
                    text_en='You removed order #%s'%order.id)
                SystemLog.objects.create(user=request.user,text='order %s, deleted' % order.id)
                order.delete()

    else:
        cart.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def delete_order(request,id):
    order=get_object_or_404(Order,id=id,buyer=request.user,is_payed=False)
    SystemLog.objects.create(user=request.user,text='order %s, deleted' % order.id)

    order.delete()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
@require_POST
@csrf_exempt
def cancelOrder(request,id):
    order=get_object_or_404(Order,id=id)
    profileSeller=order.seller.get_profile()
    profileBuyer=order.buyer.get_profile()

    if profileSeller.account>=order.payed:
            profileSeller.account-=order.payed
            profileSeller.save()
            profileBuyer.account+=order.payed
            payed= order.payed
            profileBuyer.save()
            order.cancelReason=request.POST['note']
            order.is_canceled=True
            order.status='Closed'
            order.refunded=order.payed
            order.payed=0
            order.save()
            sendEmail(user=order.buyer,type='cancelOrder',extra={'order':order})
            UserLog.objects.create(user=order.seller,
                text_ru=u'Вы отменили заказ #%s по причине %s'%(order.id,order.cancelReason),
                text_en='You canceled order #%s for reason %s'%(order.id,order.cancelReason))
            UserLog.objects.create(user=order.buyer,
                text_ru=u'Продавец %s отменил заказ #%s по причине %s'%(order.seller,order.id,order.cancelReason),
                text_en='Seller %s canceled order #%s for reason %s'%(order.seller,order.id,order.cancelReason))
            if payed:
                messages.success(request,_(u'Деньги с вашого счета перечислены обратно на счет покупателя ')+order.buyer.username)
            else:
                messages.success(request,_(u'Заказ отменен'))
    else:
            messages.error(request,_(u'Не достаточно денег'))

    return HttpResponseRedirect(request.META['HTTP_REFERER']+'?tab=third')

@login_required
def delete_address(request,id):
    address=get_object_or_404(request.user.get_profile().addresses,id=id)
    SystemLog.objects.create(user=request.user,text='addresses %s, deleted' % address.id)
    address.delete()
    return HttpResponseRedirect(reverse('cart'))

@login_required
def pay(request,id):
    order=get_object_or_404(request.user.get_profile().orders,id=id)
    profile =request.user.get_profile()
    if order.is_payed:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    if profile.account >= order.price():
        for cart in order.carts.all():
            if cart.quantity>cart.product.quantity:
                messages.error(request, _(u'Максимально доступное количество товара ')+cart.product.name+' '+str(cart.product.quantity))
                return HttpResponseRedirect(reverse('orders'))
            else:
                cart.product.quantity -=cart.quantity
                cart.product.bought += cart.quantity
                cart.product.deals +=1
                cart.product.save()

        profile.account -= order.price()
        order.payed = order.price()
        profile.save()

        seller_profile=order.seller.get_profile()
        seller_profile.account+=order.price()
        seller_profile.save()

        order.is_payed = True
        order.payed_date=datetime.now()
        order.status = 'Payed'
        order.save()

        UserLog.objects.create(user=order.seller,
            text_en='User %s pay <a href="shop/orders/">for order #%s</a>'%(order.buyer,order.id),
            text_ru=u'Пользователь %s оплатил <a href="shop/orders/">заказ #%s</a>'%(order.buyer,order.id))
        UserLog.objects.create(user=order.buyer,
            text_en='Payed for  <a href="/orders/">order #%s</a>'%order.id,
            text_ru=u'Оплачен <a href="/orders/">заказ #%s</a>'%order.id)
        SystemLog.objects.create(user=request.user,text='Pay for order %s'%order.id)
        sendEmail(user=order.seller,type="payedSeller",extra={'buyer':order.buyer,'order':order})
        sendEmail(user=order.buyer,type="payedBuyer",extra={'seller':order.seller,'order':order})
        messages.success(request,_(u'Заказ оплачен'))
        return HttpResponseRedirect(reverse('orders')+'?tab=second')
    else:
        SystemLog.objects.create(user=request.user,text='Pay for order %s, but not anough money'%order.id)
        messages.error(request,_(u'У вас на счету недостаточно средств'))

    return HttpResponseRedirect(reverse('orders')+'?tab=second')

@login_required
def confirm_delivering(request,id):
    order =  get_object_or_404(request.user.get_profile().orders,id=id)
    order.release_money()

    UserLog.objects.create(user=order.seller,
        text_en='Customer %s confirm delivery for <a href="shop/orders/">order #%s</a>'%(order.buyer,order.id),
        text_ru=u'Покупатель %s подтвердил доставку <a href="shop/orders/">заказа #%s</a>'%(order.buyer,order.id))
    UserLog.objects.create(user=order.buyer,
        text_en='Confirmed delivery for <a href="/orders/">order #%s</a>'%order.id,
        text_ru=u'Подтверждена доставка <a href="/orders/">заказа #%s</a>'%order.id)

    SystemLog.objects.create(user=request.user,text='Confirm delivery for order %s'%order.id)

    return HttpResponseRedirect(request.META['HTTP_REFERER']+'?tab=third')

@login_required
@csrf_exempt
def payments(request):
    payments = UserLog.objects.filter(user=request.user,type='payment')
    return render_to_response('cart/payments.html',{'payments':payments},context_instance=RequestContext(request))

@login_required
def make_payment(request):
    amount = request.GET['amount']
    paypal_dict = {
        "business": "vn_1337243395_biz@xoposho.com",
        "amount": str(amount),
        "item_name": str(request.user.username),
        "invoice": str(random.randint(0,1000)),
        "cancel_return": settings.ADDRESS+"/payments/",
        }
    from paypal.standard.forms import PayPalPaymentsForm
    paypal= PayPalPaymentsForm(initial=paypal_dict)

    liq=Liqpay(settings.MERCHANT_ID,settings.SIGNATURE)
    xml=liq.build_merchant_xml(order_id=str(random.randint(0,99999)),
                               amount=amount, currency=settings.CURRENCY,
        description='Add money to account: '+request.user.username,
        server_url='http://ywaga.com/payment/get_liqpay/?username='+request.user.username,
        result_url='http://ywaga.com/payments/?payment=ok',
        default_phone=settings.PHONE,
    )
    liqpay = '''<form action="https://www.liqpay.com/?do=clickNbuy" method="POST" id="form_liqpay"/>
                        <input type="hidden" name="operation_xml" value="%s" />
                        <input type="hidden" name="signature" value="%s" />
                        <button class="btn btn-success btn-large" id="liqpay_pay">Liqpay</button>
                      </form>''' % (xml.encoded_xml,xml.encoded_signature)

    return render_to_response('cart/make_payment.html',{'paypal':paypal,'liqpay':liqpay,'amount':amount},context_instance=RequestContext(request))

