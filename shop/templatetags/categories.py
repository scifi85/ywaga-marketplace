from django import template
from shop.models import TBCategoriesName
register = template.Library()

@register.filter(name='show')
def show(value,arg):
    get=TBCategoriesName.objects.filter
    name = get(id=value)

    if name:
        name=name[0]
    else:
        return value

    if arg=='ru':
        name=name.ru_name
    if arg=='en':
        name=name.en_name
    if arg=='cn':
        name=name.en_name
    return name

