# cart/models.py

from django.db import models
from shopapp.models import Product, ProductOption
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    option = models.ForeignKey(ProductOption, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def total_price(self):
        # คำนวณราคา รวม (รวมราคาของตัวเลือก ถ้ามี)
        price = self.product.price
        if self.option:
            price = self.option.product.price  # ปรับตามตัวเลือก
        return price * self.quantity

    def carbon_reduction(self):
        # คำนวณการลดคาร์บอน
        return self.product.carbon_reduction * self.quantity
