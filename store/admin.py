from django.contrib import admin
from .models import Product, Variation


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'Variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'Variation_category', 'variation_value', 'is_active')


# Register your models here.
admin.site.register(Product, ProductsAdmin)
admin.site.register(Variation,VariationAdmin)
