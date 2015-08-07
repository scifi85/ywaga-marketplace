from django.contrib import admin
from news.models import *

class NewsAdmin(admin.ModelAdmin):
    list_display = ('name','short','date')
    fieldsets = (
        (None, {
            'fields': ('name_en','name_ru','short_en','short_ru','long_en','long_ru')
            ,
            }),
        )


admin.site.register(NewsItem,NewsAdmin)



