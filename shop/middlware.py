import random
from django.conf import settings
import re
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import activate

CART_ID_SESSION_KEY = 'cart_id'
def _generate_cart_id():
    cart_id = ''
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
    cart_id_length = 50
    for y in range(cart_id_length):
        cart_id += characters[random.randint(0, len(characters)-1)]
    return cart_id

def cart_id(request):
    if request.session.get(CART_ID_SESSION_KEY,'') == '':
        request.session[CART_ID_SESSION_KEY] = _generate_cart_id()
    return request.session[CART_ID_SESSION_KEY]


class addCartId(object):
    def process_request(self, request):
        if (not 'admin' in request.build_absolute_uri()) and (not 'rosetta' in request.build_absolute_uri()):
            if not 'cart_id' in request.session:
                request.session['cart_id']=cart_id(request)

            if request.user.is_authenticated():
                if request.user.get_profile().cart_id:
                    request.session['cart_id'] = request.user.get_profile().cart_id
                else:
                    request.user.get_profile().cart_id=cart_id(request)
                    request.user.get_profile().save()


from django.conf import settings
import re

class SubdomainsMiddleware:
    def process_request(self, request):
        # if request.user.is_authenticated():
        #     if '/i18n/setlang/' in request.build_absolute_uri():
        #         profile=request.user.get_profile()
        #         profile.lang=request.POST['language']
        #         profile.save()
        activate("ru")
        request.domain = request.META['HTTP_HOST']
        request.subdomain = ''
        parts = request.domain.split('.')
        if parts[0]=='www':
            del parts[0]
        if parts[0]=='test':
            del parts[0]
        if len(parts) == 3 or (re.match("^localhost", parts[-1]) and len(parts) == 2):
            request.subdomain = parts[0]
            request.domain = '.'.join(parts[1:])


