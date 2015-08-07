# -*- encoding: utf-8 -*-
from comments.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib import messages
from shop.models import *
from django.db.models import Q
from log.models import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.translation import ugettext_lazy as _
from notification_email import sendEmail

@login_required
def post_comment(request,id):
    product = get_object_or_404(Product,id=id)

    result= product.add_comment(request)
    if result=='Comment added':
        UserLog.objects.create(user=product.user, text_en='Posted comment %s about product %s' % (request.POST['comment'],product.name),
            text_ru=u'Получен комментарий %s о товаре <a href="/product/%s/"> %s</a>' % (request.POST['comment'],product.id,product.name))
        SystemLog.objects.create(user=request.user, text='Post comment %s about product %s, id=%s' %
                                                       (request.POST['comment'],product.name,product.id))
        sendEmail(user=product.user,type='productFeedback',
            extra={'message':request.POST['comment'],'product':product,'who':request.user})
    messages.info(request,result)
    return HttpResponseRedirect(request.META['HTTP_REFERER']+'#allComments')

@login_required
def show_chat(request,to):
    from_user = request.user
    to_user = get_object_or_404(User,username=to)
    if from_user==to_user:
        messages.error(request,_(u'Вы не можете написать сообщение самому себе'))
#        messages.error(request,_(u'Can not write email to yourself'))
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    #get existed chat
    chat= Chat.objects.filter(from_user=from_user,to_user=to_user) or Chat.objects.filter(to_user=from_user,from_user=to_user)
    if chat:
        chat=chat[0]

    msgs=None
    if chat:
        if chat.from_user==from_user:
            chat.is_from_user_read=False
        else:
            chat.is_to_user_read=False
        chat.save()
        msgs= chat.comments.all()
        msgs=Paginator(msgs,10)
        try:
            page = request.GET['page']
        except:
            page = 1

        try:
            msgs = msgs.page(page)
        except (EmptyPage, InvalidPage):
            msgs = msgs.page(msgs.num_pages)

    return render_to_response('cart/message.html',{'chat':chat,'msgs':msgs,'to':to},context_instance=RequestContext(request))

@login_required
@require_POST
def post_message(request,to):
    from_user = request.user
    to_user = get_object_or_404(User,username=to)
    if from_user==to_user:
#        messages.error(request,'can not write email to yourself')
        messages.error(request,_(u'Вы не можете написать сообщение самому себе'))
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
        #get existed chat
    chat= Chat.objects.filter(from_user=from_user,to_user=to_user) or Chat.objects.filter(to_user=from_user,from_user=to_user)
    if chat:
        chat=chat[0]

    #if chat first time then create it
    if not chat:
        chat=Chat.objects.create(from_user=from_user,to_user=to_user)

    if chat.from_user==from_user:
        chat.is_to_user_read=True
    else:
        chat.is_from_user_read=True

    file = request.FILES['file'] if 'file' in request.FILES else None
    chat.add_message(from_user,request.POST['message'],file=file)

    UserLog.objects.create(user=to_user,
        text_en='Got <a href="/show_chat/%s/">message</a> %s from user %s'%(request.user,request.POST['message'],request.user),
        text_ru=u'Получено <a href="/show_chat/%s/">сообщениe</a> %s от пользователя %s'%(request.user,request.POST['message'],request.user))
    sendEmail(user=to_user,type='message',extra={'from':request.user,'message':request.POST['message']})
    SystemLog.objects.create(user=to_user, text='Message %s from user %s to user %s'%(request.POST['message'],request.user,to_user))

    return HttpResponseRedirect(reverse('send_message',args=[to,]))
@login_required
def show_messages(request):
    chats= Chat.objects.filter(Q(from_user=request.user) | Q(to_user=request.user))
    chats=Paginator(chats,10)
    try:
        page = request.GET['page']
    except:
        page = 1

    try:
        chats = chats.page(page)
    except (EmptyPage, InvalidPage):
        chats = chats.page(chats.num_pages)

    return render_to_response('cart/show_messages.html',{'chats':chats},context_instance=RequestContext(request))



