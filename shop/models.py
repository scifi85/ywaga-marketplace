# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
import re
import itertools
from django.db.models.query import QuerySet
from comments.models import *
from PIL import Image as PILImage
from django.conf import settings
from datetime import *
from django.utils.translation import ugettext as _
import random

class QuerySetManager(models.Manager):
    def get_query_set(self):
        return self.model.QuerySet(self.model)
    def __getattr__(self, attr, *args):
        return getattr(self.get_query_set(), attr, *args)



class Product(models.Model):
    COUNTRY_CHOICES =(
        ('Ukraine',_(u'Украина')),
        ('Russia',_(u'Россия')),
        ('China',_(u'Китай')),
    )
    user = models.ForeignKey(User)

    #product primary characteristics
    name = models.CharField(max_length=500)
    price = models.FloatField(default=0.00,blank=True)
    colors = models.ManyToManyField('Colors',blank=True)
    sizes = models.ManyToManyField('Sizes',blank=True)
    types = models.ManyToManyField('Types', blank=True)
    quantity = models.IntegerField(default=1)
    description = models.TextField(blank=True)
    category = models.ManyToManyField('Category',blank=True,null=True,through='Category_rel')

    images = models.ManyToManyField('Images',blank=True)
    front_images = models.ManyToManyField('Images',blank=True, related_name='front_images')
    picture = models.ImageField(upload_to='productPicture/',blank=True,null=True)

    #creation date and modify date
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    #for web
    keywords = models.ManyToManyField('Keywords',blank=True,verbose_name=_(u'Ключевый слова'))
#    meta_description = models.CharField(max_length=255,blank=True)

    #for shopping platform only
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_promotion = models.BooleanField(default=False)
    promotion_price = models.FloatField(default=0.00,blank=True,null=True)

    #Preorder
    preorder = models.BooleanField(default=False)
    preorder_days = models.IntegerField(default=0,blank=True,null=True)

    #don't know how to use yet
    self_price = models.FloatField(default=0.00,blank=True)

    #Socialize fields
    comments = models.ManyToManyField('comments.Comment',blank=True)

    #delivery prices
    # country = models.CharField(max_length=30,choices=COUNTRY_CHOICES)
    internal_delivery = models.FloatField(default=0.00,blank=True,null=True,verbose_name=_(u'Доставка по стране'))
    is_external = models.BooleanField(_(u'Доставляете за пределы своей страны ?'),default=False)
    external_delivery = models.FloatField(default=0.00,blank=True,null=True,verbose_name=_(u'Цена международной доставки'))

    bought = models.IntegerField(default=0)
    deals = models.IntegerField(default=0)
    link = models.TextField(blank=True,null=True)



    objects = QuerySetManager()

    class QuerySet(QuerySet):

        def active(self):
            return self.filter(is_active=True, is_deleted=False)

        def search(self,query):
            if query=='':
                return None
            search_result=[]
            query.encode('utf-8')
            query=query.lower()
            query = re.findall('\w+-\w+|\w+',query,re.UNICODE)
            search_templates=[]

            for phrase in itertools.permutations(query):
                template=''
                for words in phrase:
                    template+='.* '+words
                search_templates.append(template)

            for search_patern in search_templates:
                for product in self.all():
                    text=' '+product.name+' '+product.description+' '+product.user.username

                    for category in product.category.all():
                        if category.name:
                            text+=' '+category.name
                        else:
                            tb_cat= TBCategoriesName.objects.filter(id=category.number)
                            if tb_cat:
                                tb_cat=tb_cat[0]
                            text+=' '+tb_cat.cn_name+' '+tb_cat.en_name+' '+tb_cat.ru_name

                    for keyword in product.keywords.all():
                        text +=' '+keyword.keyword
                    for color in product.colors.all():
                        text +=' '+color.color
                    for size in product.sizes.all():
                        text +=' '+size.size
                    for type in product.types.all():
                        text +=' '+ type.name
                    for barcode in product.barcodes():
                        text +=' '+ barcode.number
                    text=text.lower()

                    if re.findall(search_patern,text):
                        if not product in search_result:
                            search_result.append(product)

            return search_result

        def search_by_categories(self,query):
            products = self
            for category in query:
                products = products.filter(category_rel__category__number=category)

            for product in products:
                i=0
                for category in query:
                    if not product.category.all()[i].number==int(category):
                        products=products.exclude(id=product.id)
                        break
                    i+=1

            return products.filter(is_active=True, is_deleted=False)

    class Meta:
        ordering = ['-id']

    def save(self, *args, **kwargs):
        super(Product, self).save()
        pic=self.front_images.all()

        if pic:
            self.picture = pic[0].picture
        else:
            self.picture ='nopic.png'
        super(Product, self).save()

    def is_allowed_comment(self,user):
        if user.is_authenticated():
            bought =  user.get_profile().orders.filter(carts__product=self).exclude(track_code=None)
            comment = self.comments.filter(user=user)
            today = datetime.now()
            if bought.count()>comment.count():# and (today-bought[0].sent_date).days<30:
                return True
        return False

    def recomended_products(self):
        products = Product.objects.filter(user=self.user,is_active=True, is_deleted=False).exclude(id=self.id)
        a=list(products)
        random.shuffle(a)
        return a[:5]

    def add_comment(self,request):
        if request.method=='POST' and self.is_allowed_comment(request.user):
            if 'comment' in request.POST and 'rate' in request.POST:
                if request.POST['comment']:
                    from comments.models import Comment
                    comment = Comment.objects.create(text=request.POST['comment'],user=request.user)

                    try:
                        rate=int(request.POST['rate'])
                        comment.rate=rate
                        seller=self.user.get_profile()
                        if seller.rate==None:
                            seller.rate=0
                        seller.rate+=rate
                        seller.save()
                        comment.save()
                    except :
                        pass
                    self.comments.add(comment)
                    self.save()
                    return u'Коментарий добавлен'
                return _(u'Комментарий не может быть пустым')
            else:
                return _(u'Нет комментариев в запросе')
        else:
            return _(u'Запрос не POST или комментирования запрещенно.')
        
    def __unicode__(self):
        return self.name

    # def picture(self):
    #     """
    #     Return link to the first page big picture
    #     """
    #     pic=self.front_images.all()
    #
    #     if pic:
    #         return pic[0].picture
    #     return 'nopic.png'

    def small_picture(self):
        """
        Return link to the first page small picture
        """
        pic=self.front_images.all()

        if pic:
            return pic[0].small_picture
        return 'nopic.png'

    def show_small_picture(self):
        return '<img src="/media/%s" width="64px">'% self.small_picture()
    show_small_picture.allow_tags = True

    def show_description(self):
        return self.description
    show_description.allow_tags = True

    def has_own_category(self):
        last= self.category.all()
        last = last[last.count()-1]

        if last.name=='Other' or last.number:
            return False
        flag=0
        for cat in self.category.all():
            if flag>=1:
                flag+=1
            if cat.name=='Other' or cat.number:
                flag=1

        return flag
    def category_show(self):
        n=''
        for x in  self.category.all():
            n += TBCategoriesName.objects.get(id=x.number).ru_name.encode('utf-8') + ' / '
        return n[:-2]
    def barcodes(self):
        return Barcode.objects.filter(product=self)

class Category_rel(models.Model):
    product  = models.ForeignKey('Product')
    category = models.ForeignKey('Category')
    modify_date = models.DateTimeField(auto_now=True)

class Category(models.Model):
    name = models.CharField(max_length=1000)
    number = models.IntegerField()

    def __unicode__(self):
        return self.name



class Barcode(models.Model):
    product = models.ForeignKey(Product)
    number = models.CharField(max_length=50)

class Images(models.Model):
    user = models.ForeignKey(User)
    picture = models.ImageField(upload_to = 'photos/storage/')
    small_picture = models.ImageField(upload_to = 'photos/storage/small/',blank=True,null=True)
    order_mark = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super(Images, self).save()

        if self.picture :
            t = PILImage.open(settings.MEDIA_ROOT+str(self.picture))
#            t = t.convert("RGB")
            w = float(t.size[0])
            h = float(t.size[1])
            d=w/h
            h=int(640/d)
            t = t.resize((640, h), PILImage.ANTIALIAS)
            ts = t.resize((64, h/10), PILImage.ANTIALIAS)
            new_path = 'photos/storage/small/'+str(self.picture).split('/',3)[2]
            self.small_picture=new_path
            t.save(settings.MEDIA_ROOT+str(self.picture), 'JPEG')
            ts.save(settings.MEDIA_ROOT+new_path, 'JPEG')
        super(Images, self).save()
    class Meta:
        ordering = ['order_mark','id']

class Keywords(models.Model):
    keyword= models.CharField(max_length=100)
    def __unicode__(self):
        return self.keyword

class Colors(models.Model):
    color = models.CharField(max_length=50)
    price =models.FloatField(default=0.00,blank=True)

class Sizes(models.Model):
    size = models.CharField(max_length=50)
    price =models.FloatField(default=0.00,blank=True)

    def __unicode__(self):
        return self.size

class Types(models.Model):
    name = models.CharField(max_length=50)
    price =models.FloatField(default=0.00,blank=True)

class TBCategoriesName(models.Model):
    cn_name = models.CharField(max_length=800)
    en_name = models.CharField(max_length=800)
    ru_name =  models.CharField(max_length=800)

    def __unicode__(self):
        return self.ru_name