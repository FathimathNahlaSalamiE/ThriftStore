from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(CategoryDb)


@admin.register(ProductDb)
class ProductAdmin(admin.ModelAdmin):
    exclude = ('product_seller',)

    def save_model(self, request, obj, form, change):

        # Set seller only when product is first created
        if not change:
            obj.product_seller = request.user

        super().save_model(request, obj, form, change)