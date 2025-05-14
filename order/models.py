# order/models.py
from django.db import models
from django.contrib.auth.models import User
from shopapp.models import Product, ProductOption
from cart.models import Cart

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=100, default='ชื่อผู้รับ')
    province = models.CharField(max_length=100, default='จังหวัด')
    district = models.CharField(max_length=100, default='อำเภอ')
    sub_district = models.CharField(max_length=100, default='ตำบล/เขต')
    postal_code = models.CharField(max_length=10, default='00000')
    address_detail = models.TextField(default='บ้านเลขที่/หมู่บ้าน/ถนน')
    note = models.TextField(blank=True, default='')
    phone_number = models.CharField(max_length=15, default='0000000000')
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f"{self.full_name} - {self.address_detail}, {self.sub_district}, {self.district}, {self.province}"

    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).exclude(id=self.id).update(is_default=False)
        super().save(*args, **kwargs)

class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'รอดำเนินการ'),
        ('PROCESSING', 'กำลังดำเนินการ'),
        ('SHIPPED', 'จัดส่งแล้ว'),
        ('DELIVERED', 'จัดส่งสำเร็จ'),
        ('CANCELLED', 'ยกเลิก'),  # Added CANCELLED status
    )
    PAYMENT_STATUS_CHOICES = (
        ('PENDING', 'รอชำระเงิน'),
        ('COMPLETED', 'ชำระเงินแล้ว'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_carbon_reduction = models.FloatField(default=0.0)
    promptpay_id = models.CharField(max_length=20, blank=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    option = models.ForeignKey(ProductOption, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        product_name = self.product.name if self.product else 'No Product'
        option_name = self.option.name if self.option else 'No Option'
        return f"{self.quantity} x {product_name} ({option_name})"