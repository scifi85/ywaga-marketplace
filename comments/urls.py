from django.conf.urls.defaults import *

from comments.views import *

urlpatterns = patterns('',

    url(r'post_comment/(?P<id>\d+)/$',post_comment,name='post_comment'),


    url(r'show_chat/(?P<to>\w+)/$',show_chat,name='send_message'),
    url(r'post_message/(?P<to>\w+)/$',post_message,name='post_message'),

    url(r'show_messages/$',show_messages,name='show_messages'),





)