from django.contrib import admin
from .models import Product, ProductOption, SaleInformation

class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 1

class SaleInformationInline(admin.TabularInline):
    model = SaleInformation
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'carbon_reduction', 'is_on_sale', 'discount_percentage']  # Add these
    inlines = [ProductOptionInline, SaleInformationInline]

    def is_on_sale(self, obj): # Function to display if on sale
        try:
            return obj.sale_informations.first().is_on_sale
        except:
            return False
    is_on_sale.boolean = True
    is_on_sale.short_description = 'On Sale'

    def discount_percentage(self, obj): # Function to display discount
         try:
            return obj.sale_informations.first().discount_percentage
         except:
             return None
    discount_percentage.short_description = 'Discount (%)'

admin.site.register(ProductOption)
admin.site.register(SaleInformation)