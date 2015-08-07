import sys
from datetime import date
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "ywaga.settings"
from django.core.management import setup_environ
import settings
setup_environ(settings)
DJANGO_SETTINGS_MODULE=settings


d= date(int(sys.argv[3]),int(sys.argv[2]),int(sys.argv[1]))
id= int(sys.argv[4])
from ywaga.cart.models import *

from ywaga.comments.models import *

c=Complain.objects.get(id=id)
comment= c.comments.all()[0]
comment.create_date=d
comment.save()