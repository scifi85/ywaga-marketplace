# -*- encoding: utf-8 -*-
import datetime
import random
import re
import hashlib

from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from shop.models import *
from cart.models import *
from comments.models import Chat

SHA1_RE = re.compile('^[a-f0-9]{40}$')


class RegistrationManager(models.Manager):   
    def activate_user(self, activation_key):        
        if SHA1_RE.search(activation_key):
            try:
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False
            if not profile.activation_key_expired():
                user = profile.user
                user.is_active = True
                user.save()
                profile.activation_key = self.model.ACTIVATED
                profile.save()
                return user
        return False
    
    def create_inactive_user(self, username, password, email,
                             send_email=False, profile_callback=None):
               
        new_user = User.objects.create_user(username, email, password)
        #new_user.first_name = name
        new_user.is_active = True
        new_user.save()
        
        registration_profile = self.create_profile(new_user)
        
        if profile_callback is not None:
            profile_callback(user=new_user)
        
        if send_email:
            from django.core.mail import send_mail
            current_site = Site.objects.get_current()            
            subject = render_to_string('registration/activation_email_subject.txt',
                                       { 'site': current_site })
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            #url=url.replace('&amp;','&')
            message = render_to_string('registration/activation_email.txt',
                                       { 'activation_key': registration_profile.activation_key,
                                         'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                                         'site': current_site,
                                          })
            
            #message='http://localhost:8000/accounts/activate/'+str(registration_profile.activation_key)+'/?next='+url

            #print message
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [new_user.email])
        return new_user
    
    def create_profile(self,user):
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        activation_key = hashlib.sha1(salt+user.username).hexdigest()
        return self.create(user=user, activation_key=activation_key)
        
    def delete_expired_users(self):        
        for profile in self.all():
            if profile.activation_key_expired():
                user = profile.user
                if not user.is_active:
                    user.delete()


class RegistrationProfile(models.Model):    
    ACTIVATED = u"ALREADY_ACTIVATED"
    
    user = models.ForeignKey(User, unique=True, verbose_name=_('user'))
    activation_key = models.CharField(_('activation key'), max_length=40)
    name = models.CharField(max_length=500,blank=True, verbose_name=_(u'Имя'))
    country = models.CharField(max_length=50,blank=True, verbose_name=_(u'Страна'))
#    region = models.CharField(max_length=50,blank=True)
#    street = models.CharField(max_length=200,blank=True)
#    zip_code = models.CharField(max_length=20,blank=True)
#    city = models.CharField(max_length=50,blank=True)

    address = models.TextField(blank=True,verbose_name=_(u'Адрес'))
    skype= models.CharField(max_length=50,blank=True)
    phone = models.CharField(max_length=20,blank=True, verbose_name=_(u'Телефон'))
    deposit = models.FloatField(default=0.0,blank=True)
    orders= models.ManyToManyField(Order,blank=True)
    addresses= models.ManyToManyField(Address,blank=True)
    cart_id = models.CharField(max_length=50, blank=True)
    shop_name = models.CharField(max_length=50, blank=True)
    account =  models.FloatField(default=0.0, blank=True)
    objects = RegistrationManager()
    shop_rate = models.FloatField(default=0.0,blank=True)
    buyer_rate = models.FloatField(default=0.0,blank=True)
    lang = models.CharField(max_length=10,blank=True,null=True)
    description =models.TextField(blank=True,null=True, verbose_name=_(u'Описание'))
    rate = models.IntegerField(default=0)

    class Meta:
        verbose_name = _('registration profile')
        verbose_name_plural = _('registration profiles')
    
    def __unicode__(self):
        return u"%s" % self.user
    
    def email(self):
		return self.user.email



    def is_trustable(self):
        if self.trustable:
            return '<span class="trustable"></span>'
        return ''

    def is_new_messages(self):
        chats = Chat.objects.filter(from_user=self.user)
        for chat in chats:
            if chat.is_from_user_read:
                return True
        chats = Chat.objects.filter(to_user=self.user)
        for chat in chats:
            if chat.is_to_user_read:
                return True
        return False

    def shop(self):
#        if self.trustable:
        name= '<a href="http://%s.ywaga.com" style="color:#51A351;">%s</a>'%(self.user.username,self.user.username)
#        else:
#            name= '<a href="http://%s.ywaga.com">%s</a>'%(self.user.username,self.user.username)
        rate = self.rate
        if rate>4:
            if rate in range(5,25):
                name += '<a href="http://ywaga.com/" class="lvl1 rate"></a>'
            if rate in range(25,125):
                name += '<a href="http://ywaga.com/" class="lvl2 rate" title="rate 25-124"></a>'
            if rate in range(125,625):
                name += '<a href="http://ywaga.com/" class="lvl3 rate" title="rate 125-624"></a>'
            if rate in range(625,3125):
                name += '<a href="http://ywaga.com/" class="lvl4 rate" title="rate 624-3124"></a>'
            if rate > 3124:
                name += '<a href="http://ywaga.com/" class="lvl5 rate" title="rate 3124+"></a>'
#        if self.trustable:
#            name+='<a href="#" class="trust"> <img src="/static/img/trustable.png" alt=""></a>'

        return name

#        shop.allow_tags=True

    def payed(self):
        return self.orders.filter(is_payed=True)

    def not_payed(self):
        return self.orders.filter(is_payed=False)

    def allOrders(self):
        return self.orders.all()

    def carts_in_order(self):
        result=[]
        for order in self.orders.all():
            for cart in order.carts.all():
                result.append(cart)
        return result
    def registered(self):
        return self.user.date_joined

    def activation_key_expired(self):
        expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        return self.activation_key == self.ACTIVATED or \
               (self.user.date_joined + expiration_date <= datetime.datetime.now())
    activation_key_expired.boolean = True
