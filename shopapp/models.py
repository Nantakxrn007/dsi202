# shopapp/models.py
from django.db import models

class Product(models.Model):
    # Define category choices
    CATEGORY_CHOICES = [
        ('GENERAL', 'ของใช้ทั่วไป'),
        ('CLOTHING', 'เครื่องแต่งกาย'),
        ('KITCHEN', 'เครื่องครัว'),
        ('PLANT', 'ต้นไม้'),
    ]
    
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    carbon_reduction = models.DecimalField(
        max_digits=6, decimal_places=2, default=0.00,
        help_text="จำนวนคาร์บอนที่ลดได้ (กิโลกรัม)"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='GENERAL',
        help_text="หมวดหมู่ของสินค้า"
    )

    def __str__(self):
        return self.name

class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product.name} - {self.name}"

class SaleInformation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sale_informations')
    is_on_sale = models.BooleanField(default=False)
    discount_percentage = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Sale Info for {self.product.name} (ID: {self.id})"