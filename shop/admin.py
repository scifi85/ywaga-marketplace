from django.contrib import admin
from shop.models import *

class TBCategoriesNameAdmin(admin.ModelAdmin):
    list_display = ('id','cn_name','en_name','ru_name')
    search_fields = ('id','en_name','ru_name')
admin.site.register(TBCategoriesName,TBCategoriesNameAdmin)

class ProductsShow(admin.ModelAdmin):
    list_display = ('id','name','show_description','show_small_picture','user','category_show')
    search_fields = ('id','name')

    def queryset(self, request):
        qs = super(ProductsShow, self).queryset(request)
        return qs.active()

admin.site.register(Product,ProductsShow)

