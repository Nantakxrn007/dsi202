# cart/admin.py

from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1  # เพิ่มฟอร์มสำหรับ CartItem

    fields = ('product', 'option', 'quantity', 'total_price', 'carbon_reduction')

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'total_price')
    inlines = [CartItemInline]

    def total_price(self, obj):
        return sum(item.total_price() for item in obj.items.all())

    total_price.short_description = 'Total Price'

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
