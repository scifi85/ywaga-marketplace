from django.conf.urls.defaults import *
from statistic.views import *

urlpatterns = patterns('',
    url(r'balance/$',showBalance),
)
