from django.shortcuts import render_to_response
from log.models import *
from django.template import RequestContext

def wall_more(request):
    records = UserLog.objects.filter(user=request.user)
    return render_to_response('cart/wallMore.html',{'records':records},context_instance=RequestContext(request))

