#Reset

import os
os.environ["DJANGO_SETTINGS_MODULE"] = "ywaga.settings"
from django.core.management import setup_environ
import settings
setup_environ(settings)
DJANGO_SETTINGS_MODULE=settings

from ywaga.cart.models import *
Order.objects.all().delete()
CartItem.objects.all().delete()

from ywaga.comments.models import *
#Complain.objects.all().delete()
Comment.objects.all().delete()
Chat.objects.all().delete()

from ywaga.statistic.models import Balance
Balance.objects.all().delete()

from ywaga.log.models import *
SystemLog.objects.all().delete()
UserLog.objects.all().delete()

from ywaga.registr.models import *
for profile in RegistrationProfile.objects.all():
    profile.account=0.0
    profile.save()

from payments.models import *
Payment.objects.all().delete()


