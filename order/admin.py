from django.contrib import admin
from .models import Order, OrderItem, Address

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_status')
    search_fields = ('id', 'user__username')
    readonly_fields = ('id', 'created_at', 'updated_at')
    fields = (
        'user', 'cart', 'address', 'total_price', 'total_carbon_reduction',
        'status', 'payment_status', 'promptpay_id', 'qr_code', 'created_at', 'updated_at'
    )
    list_editable = ('status', 'payment_status')  # Allow direct editing in list view

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'option', 'quantity', 'price')
    search_fields = ('order__id', 'product__name')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'province', 'district', 'sub_district', 'is_default')
    list_filter = ('is_default',)
    search_fields = ('user__username', 'full_name', 'address_detail')