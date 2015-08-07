from django.contrib import admin
import datetime
from comments.models import *
from django.contrib import messages

class ChatShow(admin.ModelAdmin):
    list_display = ('from_user','to_user')
    change_form_template='admin/comments/change_form_comments.html'
    exclude = ('comments',)
admin.site.register(Chat,ChatShow)

