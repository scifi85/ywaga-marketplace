import os
os.environ["DJANGO_SETTINGS_MODULE"] = "ywaga.settings"
from django.core.management import setup_environ
import settings
setup_environ(settings)
DJANGO_SETTINGS_MODULE=settings

from django.contrib.auth.models import User
from ywaga.log.models import *

user=User.objects.get(id=1)
SystemLog.objects.create(text='hi',user=user)
