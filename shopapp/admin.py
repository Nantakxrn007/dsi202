# admin.py
from django.contrib import admin
from .models import Product, ProductOption

class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'carbon_reduction']
    inlines = [ProductOptionInline]

admin.site.register(ProductOption)