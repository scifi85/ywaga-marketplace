# -*- encoding: utf-8 -*-
from django import template
from cart.models import *
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from shop.models import *

register = template.Library()

@register.simple_tag(takes_context=True)
def cartLen(context):
    carts=CartItem.objects.filter(cart_id=context['request'].session['cart_id'])

    return carts.count()

@register.filter(name='statusTrans')
def statusTrans(status,lang):
    if lang=='ru':
        if status=='Closed':
            return 'Закрыто'
        if status=='Not payed':
            return '<span class="np">Не оплачено</span>'
        if status=='Payed':
            return '<span class="pd">Оплачено</span>'
        if status=='Sent':
            return '<span class="sn">Отправлено</span>'
    else:
        if status=='Closed':
            return 'Closed'
        if status=='Not payed':
            return '<span class="np">Not payed</span>'
        if status=='Payed':
            return '<span class="pd">Payed</span>'
        if status=='Sent':
            return '<span class="sn">Sent</span>'


@register.filter(name='complainTrans')
def complainTrans(status,lang):
    if lang=='ru':
        if status=='Open':
            return '<span class="go">Открыто</span>'
        if status=='Closed':
            return '<span class="gz">Закрыто</span>'
    else:
        return status

@register.filter(name='countryTrans')
def countryTrans(status,lang):
    if not status:
        return ''
    if lang=='ru':
        if status=='Ukraine':
            return 'Украина'
        if status=='Russia':
            return 'Россия'
        if status=='China':
            return 'Китай'
    else:
        return status

@register.filter(name='colorTrans')
def colorTrans(color,lang):
    if lang=='ru':
        if color=='black':
            return 'черный'
        if color=='dark grey':
            return 'серый темный'
        if color=='grey':
            return 'серый'
        if color=='light grey':
            return 'серый светлый'
        if color=='white':
            return 'белый'
        if color=='dark pink':
            return 'розовый темный'
        if color=='pink':
            return 'розовый'
        if color=='light pink':
            return 'розовый светлый'
        if color=='coral':
            return 'коралловый'
        if color=='dark red':
            return 'красный темный'
        if color=='red':
            return 'красный'
        if color=='orange':
            return 'оранжевый'
        if color=='taupe':
            return 'серо-коричневый'
        if color=='brown':
            return 'коричневый'
        if color=='beige':
            return 'беж'
        if color=='blue-green':
            return 'сине-зеленый'
        if color=='olive':
            return 'оливковый'
        if color=='dark green':
            return 'зеленый темный'
        if color=='green':
            return 'зеленый'
        if color=='light green':
            return 'зеленый светлый'
        if color=='turquoise':
            return 'бирюзовый'
        if color=='azure':
            return 'голубой'
        if color=='light blue':
            return 'синий светлый'
        if color=='electric blue':
            return 'синий электрик'
        if color=='dark blue':
            return 'синий темный'
        if color=='indigo':
            return 'индиго'
        if color=='dove-colored':
            return 'сизый'
        if color=='purple':
            return 'фиолетовый'
        if color=='cherry':
            return 'вишневый'
        if color=='lilac':
            return 'сиреневый'
        if color=='dark yellow':
            return 'желтый темный'
        if color=='yellow':
            return 'желтый'
        if color=='light yellow':
            return 'желтый светлый'
    else:
        return color

from django.template.defaulttags import url as url_orig

@register.tag
def url(parser, token):
    class URLNode(template.Node):
        def __init__(self, origURLNode):
            self.origURLNode=origURLNode

        def render(self, context):
            if 'shop' in token.contents.split(' '):
                shop = parser.compile_filter(token.contents.split(' ')[2]).resolve(context)
                return 'http://'+shop+'.'+settings.ADDRESS

            return 'http://'+settings.ADDRESS+self.origURLNode.render(context)

    return URLNode(url_orig(parser, token))

@register.simple_tag
def count_number(cid):
    return Product.objects.active().filter(category__number=cid).count()

@register.filter(name='recommended_product')
def recommended_product(id):
    product = Product.objects.get(id=id)
    return product

@register.inclusion_tag('admin/formOrder/cartsOrder.html',takes_context=True)
def display_carts(context,id):
    order = Order.objects.get(id=id)
    carts = order.carts.all()
    #    groups = context['request'].user.groups.all()
    #    groups = [group.name for group in groups]
    #    superuser=context['request'].user.is_superuser
    return { 'carts': carts,'order':order,'user':context['request'].user }






