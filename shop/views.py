# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect,Http404
from shop.models import *
from shop.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from categories import *
import re
import simplejson
from django.core.urlresolvers import reverse
from cart.models import *
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from log.models import *
from taobao import *
import urllib2
from translate import translate
from shop.categoryTree import *
from django.utils import translation
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from notification_email import *
import random
from threading import Thread
from thread import *

@login_required
def show_products(request):
    products = Product.objects.filter(user=request.user, is_deleted=False)
    query =''
    if 'search' in request.GET:
        query=request.GET['search']
        products = products.search(query)
    products=Paginator(products,60)
    try:
        page = request.GET['page']
    except:
        page = 1
    try:
        products = products.page(page)
    except (EmptyPage, InvalidPage):
        products = products.page(products.num_pages)

    return render_to_response('manage_shop/search.html',{'products':products,'query':query},context_instance=RequestContext(request))

@login_required
def show_shop_orders(request):
    payed_orders = Order.objects.filter(seller=request.user,is_payed=True).exclude(status='Closed')
    not_payed_orders = Order.objects.filter(seller=request.user,is_payed=False).exclude(status='Closed')
    closed_orders=Order.objects.filter(seller=request.user,status='Closed')

    payed_orders=Paginator(payed_orders,10)
    try:
        page = request.GET['page']
    except:
        page = 1
    try:
        payed_orders = payed_orders.page(page)
    except (EmptyPage, InvalidPage):
        payed_orders = payed_orders.page(payed_orders.num_pages)

    not_payed_orders=Paginator(not_payed_orders,10)
    try:
        page2 = request.GET['page2']
    except:
        page2 = 1
    try:
        not_payed_orders = not_payed_orders.page(page2)
    except (EmptyPage, InvalidPage):
        not_payed_orders = not_payed_orders.page(payed_orders.num_pages)

    closed_orders=Paginator(closed_orders,10)
    try:
        page3 = request.GET['page3']
    except:
        page3 = 1
    try:
        closed_orders = closed_orders.page(page3)
    except (EmptyPage, InvalidPage):
        closed_orders = closed_orders.page(closed_orders.num_pages)


    return render_to_response('manage_shop/orders.html',{'payed_orders':payed_orders,'not_payed_orders':not_payed_orders,'closed_orders':closed_orders},context_instance=RequestContext(request))

@login_required
def delete_product(request,product_id):
    product= Product.objects.filter(id=product_id, user=request.user)
    product.update(is_deleted=True, is_active=False)
    if product:
        SystemLog.objects.create(user=request.user,text='Delete product id=%s, name=%s'%(product[0].id,product[0].name))
    return HttpResponseRedirect(reverse('show'))

@login_required
@require_POST
def action(request):
    if request.POST['action']=='del_all':
        products= Product.objects.filter(user=request.user)
        products.update(is_deleted=True, is_active=False)
        for product in products:
            SystemLog.objects.create(user=request.user,text='Delete product id=%s, name=%s'%(product.id,product.name))
    if request.POST['action']=='del_choosen':
        for k,v in request.POST.items():
            if 'product_' in k:
                product= Product.objects.filter(id=int(k.replace('product_','')), user=request.user)
                product.update(is_deleted=True, is_active=False)
                if product:
                    SystemLog.objects.create(user=request.user,text='Delete product id=%s, name=%s'%(product[0].id,product[0].name))

    return HttpResponseRedirect(reverse('show'))

@login_required
def add_product(request,product_id):

    #exist product or no
    product = Product.objects.filter(id=product_id, user=request.user,is_deleted=False)[0] if product_id else None

    #Create or read form
    new_product = NewProductForm(request.POST or None, instance=product or None)

    if new_product.is_valid():
        #Create new product
        product=new_product.save(commit=False)
        product.user=request.user
        if product.internal_delivery==None:
            product.internal_delivery=0.0
        if product.external_delivery==None:
            product.external_delivery=0.0
            # product.is_external=False
        if product.promotion_price==None:
            product.is_promotion=False
        if 'is_external' in request.POST:
            product.is_external=True
        else:
            product.is_external=False
        product.save()

        categories = -1
        #Handle form fields
        product.sizes.all().delete()
        for key, value in request.POST.iteritems():

            #Handle new keyword
            if 'new_keyword' in key:
                if not value=='':
                    keyword = Keywords.objects.create(keyword=value)
                    product.keywords.add(keyword)

            #handle current keywords
            if 'keyword_' in key:
                keyword_id=key.replace('keyword_','')
                keyword_id=int(keyword_id)
                if value:
                    Keywords.objects.filter(id=keyword_id).update(keyword=value)
                else:
                    Keywords.objects.filter(id=keyword_id).delete()

            #Handle new barcode
            if 'new_barcode' in key:
                if not value=='':
                    Barcode.objects.create(number=value,product=product)


            #handle current barcode
            if 'barcode_' in key:
                barcode_id=key.replace('barcode_','')
                barcode_id=int(barcode_id)
                if value:
                    Barcode.objects.filter(id=barcode_id,product=product).update(number=value)
                else:
                    Barcode.objects.filter(id=barcode_id,product=product).delete()

            if 'category' in key:
                categories +=1

            if 'colors_' in key:
                id = key.replace('colors_','')
                color = value
                if not color:
                    continue
                price = request.POST['color_price_'+str(id)]
                color = Colors.objects.create(color=color,price=price)

                product.colors.add(color)

            if 'initial_color0_' in key:
                id = key.replace('initial_color0_','')
                color=value

                if not color:
                    Colors.objects.get(id=id).delete()
                    continue
                price= request.POST['initial_color_price0_'+str(id)]
                if  not price:
                    price=product.price
                Colors.objects.filter(id=id).update(color=color,price=price)

            if 'sizes_' in key:
                size = key.replace('sizes_','')

                if not size:
                    continue
                price = request.POST['size_price_'+str(size)].replace(',','.')

                size = Sizes.objects.create(size=size,price=price)
                product.sizes.add(size)


            if 'initial_size0_' in key:
                id = key.replace('initial_size0_','')
                size=value
                if not size:
                    Sizes.objects.get(id=id).delete()
                    continue
                price= request.POST['initial_size_price0_'+str(id)]
                if  not price:
                    price=product.price
                Sizes.objects.filter(id=id).update(size=size,price=price)

            if 'types_' in key:
                id = key.replace('types_','')
                type = value
                if not type:
                    continue
                price = request.POST['type_price_'+str(id)]
                type = Types.objects.create(name=type,price=price)
                product.types.add(type)

            if 'initial_type0_' in key:
                id = key.replace('initial_type0_','')
                type=value
                if not type:
                    Types.objects.get(id=id).delete()
                    continue
                price= request.POST['initial_type_price0_'+str(id)]
                if  not price:
                    price=product.price
                Types.objects.filter(id=id).update(name=type,price=price)

            #Handle promo images from webcamera
            if 'promo_pic' in key:
                id = key.replace('promo_pic_','')
                mark = request.POST['mark_tmp_picture_'+id]
                image = Images.objects.create(picture=value,user=request.user,order_mark=mark)
                product.images.add(image)
                product.save()
            if 'frontPic_' in key:
                id = key.replace('frontPic_','')
                mark = request.POST['mark_tmp_front_picture_'+id]
                image = Images.objects.create(picture=value,user=request.user,order_mark=int(mark))

                product.front_images.add(image)
                product.save()
            if 'deletePromoPic' in key:
                image = Images.objects.get(user=request.user,id=int(value))
                product.images.remove(image)

            if 'deleteFrontPicture' in key:
                image = Images.objects.get(user=request.user,id=int(value))
                product.front_images.remove(image)
                product.save()

            if 'mark_picture_' in key:
                id= key.replace('mark_picture_','')
                Images.objects.filter(user=request.user,id=id).update(order_mark=int(value))
            if 'mark_front_picture_' in key:
                id= key.replace('mark_front_picture_','')
                Images.objects.filter(user=request.user,id=id).update(order_mark=int(value))


        for i in range(0,categories+1):
            value=request.POST['category'+str(i)]
            if i==0:
                product.category.clear()

            if not (value=='Please choose a category' or value==''):
                try:
                    category=Category.objects.filter(number=value)
                    category = category[0] if category else Category.objects.create(number=value)
                except:
                    category=Category.objects.filter(name=value)
                    category = category[0] if category else Category.objects.create(name=value)

                Category_rel.objects.create(product=product,category=category)


        #Handle promo images from file
        tid=0
        for key,value in request.FILES.iteritems():
            if 'prom_' in key:
                id = key.replace('prom_','')
                mark = request.POST['mark_tmp_picture_'+id]
                image=Images.objects.create(picture=value, user=request.user,order_mark=mark)
                product.images.add(image)
                product.save()
            if 'front_' in key:
                id = key.replace('front_','')
                try:
                    mark = request.POST['mark_tmp_front_picture_'+id]
                except :
                    mark = tid
                    tid+=1
                try:
                    image=Images.objects.create(picture=value, user=request.user,order_mark=mark)
                    product.front_images.add(image)
                    product.save()
                except :
                    messages.error(request,_(u'Error with picture, add one more time'))

        #Handle pressed
        SystemLog.objects.create(user=request.user,text='Added product id=%s, name=%s'% (product.id,product.name))
#        UserLog.objects.create(user=request.user,text='Added product id=%s, name=%s'% (product.id,product.name))

        if request.POST['save']=="SaveNew":
            return HttpResponseRedirect(reverse('add_product'))
        if request.POST['save']=="Save":
            return HttpResponseRedirect(reverse('show'))
        if request.POST['save']=="SaveContinue":
            return HttpResponseRedirect(reverse('edit_product',args=[product.id]))

    return render_to_response('manage_shop/add-product.html',{'product_form':new_product,'product':product},context_instance=RequestContext(request))

#@login_required
#def setTrust(request,trust):
#    profile=request.user.get_profile()
#    if  profile.is_choosen_trust:
#        messages.error(request,'Haha ;)')
#        SystemLog.objects.create(user=request.user,text='hack attempt, trust level again')
#        return HttpResponseRedirect(reverse('show'))
#    if trust=='true':
#        profile.is_choosen_trust =True
#        profile.trustable =True
#        profile.save()
#    elif trust=='false':
#        profile.is_choosen_trust =True
#        profile.trustable =False
#        profile.save()
#    else:
#        messages.error(request,'error')
#        SystemLog.objects.create(user=request.user,text='hack attempt, trust level')
#        return HttpResponseRedirect(reverse('show'))
#    return HttpResponseRedirect(reverse('add_product'))

@login_required
@csrf_exempt
def capture_tmp(request):
    import random
    import string

    s=''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(20))
    name='photos/tmp/%s.jpg' %s
    url=settings.ROOT_SITE+'/media/'+name
    f = open(url, 'wb')
    if request.FILES:
        for file in request.FILES:
            f.write(request.FILES[file].read())
    else:
        f.write(request.read())
    f.close()
    return HttpResponse(name)

@login_required
def get_categories(request,categories):
    TEMP = catTree

    if categories==None:
        if translation.get_language()=='en':
            resp=[(TBCategoriesName.objects.get(id=i).en_name,i) for i in TEMP.keys()]
        if translation.get_language()=='ru':
            resp=[(TBCategoriesName.objects.get(id=i).ru_name,i) for i in TEMP.keys()]
        if translation.get_language()=='cn':
            resp=[(TBCategoriesName.objects.get(id=i).cn_name,i) for i in TEMP.keys()]
        resp.sort()

        resp.insert(0,(u'Пожалуйста, выберите категорию',"Please choose a category"))
#        resp.append(('Other','Other'))
        return HttpResponse(simplejson.dumps(resp))

    categories = re.findall('<catend>(.*?)</catend>',categories)

    for i in categories:
        if i=='Other':
            continue
        i=int(i)
        if not i in TEMP.keys():
            return HttpResponse(simplejson.dumps('no category'))
        if TEMP[i]==None:
            return HttpResponse(simplejson.dumps('finished'))
        TEMP = TEMP[i]


    if translation.get_language()=='en':
        resp=[(TBCategoriesName.objects.get(id=i).en_name,i) for i in TEMP.keys()]
    if translation.get_language()=='ru':
        resp=[(TBCategoriesName.objects.get(id=i).ru_name,i) for i in TEMP.keys()]
    if translation.get_language()=='cn':
        resp=[(TBCategoriesName.objects.get(id=i).cn_name,i) for i in TEMP.keys()]

    resp.sort()

    resp.insert(0,(u'Пожалуйста, выберите категорию',"Please choose a category"))
    resp.append((u'Другое','Other'))

    return HttpResponse(simplejson.dumps(resp))

@login_required
def change(request,cart_id,value,type):
    try:
        cart=CartItem.objects.filter(product__user=request.user,id=cart_id)
        if cart:
            cart=cart[0]
        else:
            cart=CartItem.objects.get(id=cart_id)
            if not cart.order().buyer==request.user:
                raise 'Hack Attempt'

        order =cart.order()

        if order.payed and not type=='track_code':
            raise Exception('Order payed')
        if type=='quantity':
            if not cart.quantity == int(value):
                UserLog.objects.create(user=order.buyer,
                    text_ru=u'Продавец %s изменил количество товара %s с %s на %s в вашем заказе #%s' % (order.seller,cart.product.name,cart.quantity,value,order.id),
                    text_en='Seller %s change quantity for product %s from %s to %s in your order #%s' % (order.seller,cart.product.name,cart.quantity,value,order.id)
                )
                SystemLog.objects.create(user=request.user,text='Change price for product %s from %s to %s in order %s' %
                    (cart.product.name,cart.quantity,value,order.id))
                cart.quantity = int(value)
        if type=='price':
            if not cart.price==float(value):
                UserLog.objects.create(user=order.buyer,
                    text_ru=u'Продавец %s изменил цену товара %s с %s на %s в вашем заказе #%s' %(order.seller,cart.product.name,cart.price,value,order.id),
                    text_en='Seller %s changed price for product %s from %s to %s in your order #%s' %(order.seller,cart.product.name,cart.price,value,order.id)
                )
                SystemLog.objects.create(user=request.user,text='Change price for product %s from %s to %s in your order #%s' %
                                                       (cart.product.name,cart.price,value,order.id))
                cart.price = float(value)
        if type=='delivery':
            if not cart.delivery == float(value):
                UserLog.objects.create(user=order.buyer,
                    text_ru=u'Продавец %s изменил цену на доставку товара %s с %s на %s в вашем заказе #%s' % (order.seller,cart.product.name,cart.delivery,value,order.id),
                    text_en='Seller %s changed delievry price for product %s from %s to %s in your order #%s' % (order.seller,cart.product.name,cart.delivery,value,order.id)
                )
                SystemLog.objects.create(user=request.user,text='Change delivery price for product %s from %s to %s in order #%s' %
                                                           (cart.product.name,cart.delivery,value,order.id))
                cart.delivery = float(value)
        cart.save()

        resp = {'price':str(cart.full_price()), 'order_price': str(order.price()), 'order_id':order.id}
    except :
        resp='error'
    return HttpResponse(simplejson.dumps(resp))

@login_required
def upload_track_code(request,order_id):
    try:
        code = request.GET['code']
        order=Order.objects.get(id=order_id)

        order.status='Closed'
        order.track_code=code
        order.sent_date=datetime.today()
        order.save()

        profile = request.user.get_profile()
        profile.rate+=1
        profile.save()
        UserLog.objects.create(user=order.buyer,
            text_en='Seller %s put tracking code for %s for <a href="/orders/">order #%s </a>' %(order.seller,order.track_code,order.id),
            text_ru=u'Продавец %s указал трекинг код %s для <a href="/orders/">заказа #%s </a>' %(order.seller,order.track_code,order.id))
        UserLog.objects.create(user=order.seller,
            text_en='Puted tracking code %s for <a href="shop/orders">order #%s</a>'%(order.track_code,order.id),
            text_ru=u'Указан трекинг код %s для <a href="shop/orders">заказа #%s</a>'%(order.track_code,order.id))
        SystemLog.objects.create(user=request.user,
            text='Upload track id %s for order %s' %(order.track_code,order.id))

        sendEmail(user=order.buyer, type='track',extra={'seller':order.seller,'track_code':order.track_code,'order_id':order.id})
        resp = 'ok'
    except :
        resp = 'error'
    return HttpResponseRedirect(reverse('show_my_orders'))

@login_required
def contacts(request):
    from registr.forms import ContactForm
    form = ContactForm(instance=request.user.get_profile())
    if request.method=='POST':
        form = ContactForm(request.POST,instance=request.user.get_profile())
        if form.is_valid():
            form.save()
            if 'next' in request.POST:
                if request.POST['next']=='add_product':
                    return HttpResponseRedirect(reverse('add_product'))
    return render_to_response('manage_shop/contacts.html',{'form':form},context_instance=RequestContext(request))


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs, Verbose)
        self._return = None

    def run(self):
        if self._Thread__target is not None:
            self._return = self._Thread__target(*self._Thread__args,
                **self._Thread__kwargs)

    def join(self):
        Thread.join(self)
        return self._return

def attach_pic_to_product(url,product,user):
    opener = urllib2.build_opener()
    page = opener.open(url)

    filename = str(product.id)+'_'+str(random.randint(0,999999))

    filename='photos/storage/'+filename

    fout = open(settings.MEDIA_ROOT+filename, "wb")
    fout.write(page.read())
    fout.close()

    image=Images.objects.create(picture=filename, user=user,order_mark=1)

    product.front_images.add(image)
    product.save()

    return 'ok'


@login_required
@csrf_exempt
def addProductFromTB(request):

        url=request.POST['link']
        id = re.findall('id=(\d+)',url)

        if id:
            id = id[0]
            data = get_item(id,['title','price','item_img','cid'])
            name= data['title']
            name = translate(name)

        price = data['price']
        price = round(float(price) / 6.3*8.2,2)
        imgs = data['item_img']
    #        cid=data['cid']
        mark=0

        product = Product.objects.create(name=name,price=float(price),
                preorder=True,user=request.user,country='China',link=url)


#        parents= find(cid)

#        for category_id in parents:
#            category=Category.objects.filter(number=category_id)
#            category = category[0] if category else Category.objects.create(number=category_id)
#            Category_rel.objects.create(product=product,category=category)

        try:
            t={}
            for url in imgs:
                t[url]= ThreadWithReturnValue(target=attach_pic_to_product,args=(url,product,request.user))
                t[url].start()
#                attach_pic_to_product(url,product,request.user)

                mark+=1
            for url in imgs:
                t[url].join()
        except Exception,e:
            print e

        return HttpResponse(str(product.id))
#    return HttpResponseRedirect(reverse('edit_product',args=[product.id]))