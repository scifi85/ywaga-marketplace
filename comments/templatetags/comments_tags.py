from django import template
from comments.models import *

register = template.Library()


@register.inclusion_tag('admin/comments.html')
def display_comments(id):
    complain = Complain.objects.get(id=id)
    return { 'complain': complain}

@register.inclusion_tag('admin/comments/comments.html',takes_context = True)
def displayChat(context,id):
    comments = Chat.objects.get(id=id).comments.all()
    return { 'comments': comments}
