from django.contrib import admin

from registr.models import RegistrationProfile


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','account','registered')

    fieldsets = (
        (None, {
            'fields': ('user','cart_id','shop_name','account'),
            }),
        )


admin.site.register(RegistrationProfile, RegistrationAdmin)
