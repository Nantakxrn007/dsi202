from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    carbon_reduction = models.DecimalField(
        max_digits=6, decimal_places=2, default=0.00,
        help_text="จำนวนคาร์บอนที่ลดได้ (กิโลกรัม)"
    )
    is_on_sale = models.BooleanField(default=False)  # 👈 เพิ่ม field นี้
    discount_percentage = models.IntegerField(null=True, blank=True)  # 👈 เพิ่ม field นี้


    
    def __str__(self):
        return self.name

class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product.name} - {self.name}"