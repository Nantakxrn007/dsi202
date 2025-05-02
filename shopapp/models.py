from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # 👈 เพิ่มตรงนี้
    carbon_reduction = models.DecimalField(
        max_digits=6, decimal_places=2, default=0.00,
        help_text="จำนวนคาร์บอนที่ลดได้ (กิโลกรัม)"
    )

    def __str__(self):
        return self.name
    
class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product.name} - {self.name}"
    
