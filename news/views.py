from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from news.models import *

def showNews(request):
    news= NewsItem.objects.all()
    news=Paginator(news,10)
    try:
        page = request.GET['page']
    except:
        page = 1

    try:
        news = news.page(page)
    except (EmptyPage, InvalidPage):
        news = news.page(news.num_pages)

    return render_to_response('news/showAll.html',{'news':news},context_instance=RequestContext(request))

def showOne(request,id):
    item = get_object_or_404(NewsItem,id=id)
    return render_to_response('news/showOne.html',{'item':item},context_instance=RequestContext(request))