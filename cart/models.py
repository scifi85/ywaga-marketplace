# -*- encoding: utf-8 -*-
from django.db import models
from shop.models import *
from comments.models import *
from datetime import *
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _
# from notification_email import sendEmail
from log.models import *

class QuerySetManager(models.Manager):
    def get_query_set(self):
        return self.model.QuerySet(self.model)
    def __getattr__(self, attr, *args):
        return getattr(self.get_query_set(), attr, *args)



class CartItem(models.Model):
    cart_id = models.CharField(max_length=50)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey('shop.Product')
    price = models.FloatField(default=0.00,blank=True)
    delivery = models.FloatField(default=0.00,blank=True)
    color = models.ForeignKey('shop.Colors',null=True)
    size = models.ForeignKey('shop.Sizes',null=True)
    type = models.ForeignKey('shop.Types',null=True)
    objects = QuerySetManager()

    def __unicode__(self):
        return str(self.id)

    class QuerySet(QuerySet):
        def full_price(self):
            return sum([x.full_price() for x in self.all()])

        def order_by_shop(self):
            shops=[]
            class Shop:
                pass

            for item in self.all():
                flag = True
                user = item.product.user
                for x in shops:
                    if x.user  == user:
                        flag = False
                if flag:
                    shop=Shop()
                    shop.user = user
                    shop.carts = self.filter(product__user=shop.user)
                    shop.price = sum([x.full_price() for x in shop.carts])

                    shops.append(shop)

            return  shops

    def full_price(self):
        return self.price*self.quantity+self.delivery

    def order(self):
        orders= Order.objects.filter(carts=self)
        return orders[0] if orders else False

    # def complain(self):
    #     from comments.models import Complain
    #
    #     complains = Complain.objects.filter(cart=self)
    #     if complains:
    #      return complains[0]
    #
    #     return  False
    #
    # def is_allowed_complain(self):
    #     #if exist complain
    #     if self.complain():
    #         return True
    #
    #     if not self.product.user.get_profile().trustable:
    #         return False
    #
    #     order = self.order()
    #     today = datetime.now()
    #
    #     #if no complain and order is expired (pass more then 14 days after sending), then return False
    #     if (order.sent_date and (today-order.sent_date).days>=14) or order.status=='Closed':
    #         return False
    #
    #     return True

    def shop(self):
        return self.product.user

    class Meta:
        ordering = ['product__user','-id']



class Order(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    carts  = models.ManyToManyField(CartItem)
    is_payed = models.BooleanField(default=False)
    payed = models.FloatField(default=0.0, blank=True)
    payed_date = models.DateTimeField(blank=True,null=True)

    buyer = models.ForeignKey(User,verbose_name=_(u'Покупатель'))
    seller = models.ForeignKey(User, related_name='seller')

    sent_date = models.DateTimeField(blank=True,null=True)
    track_code = models.CharField(max_length=50)
    delivered_date =models.DateTimeField(blank=True,null=True)

    country = models.CharField(max_length=50)
    region = models.CharField(max_length=50,blank=True)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)

    status = models.CharField(max_length=100)
    is_direct_pay = models.BooleanField(default=False)

    cancelReason = models.TextField(null=True,blank=True)
    is_canceled = models.BooleanField(default=False)

    def price(self):
        return self.carts.all().full_price()

    def balance(self):
        return self.price()-self.payed#-self.released-self.refunded

    def __unicode__(self):
        return str(self.id)

    class Meta:
        ordering = ['-modify_date']

class Address(models.Model):
    country = models.CharField(max_length=50,verbose_name=_(u'Страна'))
    region = models.CharField(max_length=50,blank=True,verbose_name=_(u'Область'))
    city = models.CharField(max_length=50,verbose_name=_(u'Город'))
    street = models.CharField(max_length=200,verbose_name=_(u'Улица'))
    zip_code = models.CharField(max_length=20,verbose_name=_(u'Почтовый индекс'))
    phone = models.CharField(max_length=20,verbose_name=_(u'Телефон'))

    class Meta:
        ordering = ['-id']

