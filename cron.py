import os
os.environ["DJANGO_SETTINGS_MODULE"] = "ywaga.settings"
from django.core.management import setup_environ
import settings
setup_environ(settings)
DJANGO_SETTINGS_MODULE=settings


from datetime import *
from django.db.models import Q

from ywaga.cart.models import *
from ywaga.comments.models import *
from ywaga.log.models import *
from django.contrib.auth.models import User

user=User.objects.get(id=1)

SystemLog.objects.create(text='run script',user=user)
try:
    orders = Order.objects.filter(status='Sent')
    today = datetime.now()

    for order in orders:
        if (today - order.sent_date).days>14:
            print order.id
            order.release_money()

    complains = Complain.objects.filter(status='Open',invite_judge=False)
    for complain in complains:
            last_comment=complain.comments.all()[0]
            if (today - last_comment.create_date).days>3:
                #buyer win
                if complain.buyer==last_comment.user:
                    complain.refund_complete(win='buyer')
                #seller win
                if complain.seller==last_comment.user:
                    complain.refund_complete(win='seller')
    SystemLog.objects.create(text='finish script',user=user)
except :
    print 'error'
    SystemLog.objects.create(text='script error',user=user)



