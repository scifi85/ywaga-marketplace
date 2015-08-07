from django.conf.urls.defaults import *
from news.views import *

urlpatterns = patterns('',
    url(r'showNews/$',showNews,name='showNews'),
    url(r'news/(?P<id>\d+)/$',showOne,name='showOne')
)
