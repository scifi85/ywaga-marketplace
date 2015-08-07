from django.contrib import admin
from cart.models import *

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','buyer','seller','country','status','modify_date','track_code')
    change_form_template='admin/formOrder/change_form_order.html'
    readonly_fields = ('buyer','seller','payed','country','region','city','street','zip_code','phone')
    fieldsets = (
        (None, {
            'fields': (('buyer','seller'),'payed',('country','region','city','street','zip_code','phone')),
        }),
    )
#class CartItemAdmin(admin.ModelAdmin):

admin.site.register(Order,OrderAdmin)
admin.site.register(CartItem)


