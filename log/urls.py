from django.conf.urls.defaults import *
from log.views import *
urlpatterns = patterns('',
    url(r'wall_more/$',wall_more,name='wall_more'),
)