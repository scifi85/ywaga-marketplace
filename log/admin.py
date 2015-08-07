from django.contrib import admin
from log.models import *

class SystemLogAdmin(admin.ModelAdmin):
    list_display=('user','text','type','create_date')
admin.site.register(SystemLog,SystemLogAdmin)