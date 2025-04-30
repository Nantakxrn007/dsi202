from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # 👈 เพิ่มตรงนี้

    def __str__(self):
        return self.name