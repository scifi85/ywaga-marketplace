from django import template
from log.models import *

register = template.Library()


@register.inclusion_tag('tags/wall.html')
def display_wall(user):
    records = UserLog.objects.filter(user=user)[:10]
    return { 'records': records}
