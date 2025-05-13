# shopapp/admin.py
from django.contrib import admin
from .models import Product, ProductOption, SaleInformation , Profile

class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 1

class SaleInformationInline(admin.TabularInline):
    model = SaleInformation
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'carbon_reduction', 'category', 'is_on_sale', 'discount_percentage']
    inlines = [ProductOptionInline, SaleInformationInline]
    list_filter = ['category']  # Add category filter in admin

    def is_on_sale(self, obj):
        try:
            return obj.sale_informations.first().is_on_sale
        except:
            return False
    is_on_sale.boolean = True
    is_on_sale.short_description = 'On Sale'

    def discount_percentage(self, obj):
        try:
            return obj.sale_informations.first().discount_percentage
        except:
            return None
    discount_percentage.short_description = 'Discount (%)'

admin.site.register(ProductOption)
admin.site.register(SaleInformation)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_picture')
    search_fields = ('user__username',)