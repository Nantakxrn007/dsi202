from django.db import models
from shopapp.models import Product, ProductOption
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username if self.user else self.session_key}"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())
    
    def total_carbon_reduction(self):
        return sum(item.carbon_reduction() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    option = models.ForeignKey(ProductOption, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ('cart', 'product', 'option')

    def __str__(self):
        option_name = self.option.name if self.option else 'No Option'
        return f"{self.quantity} x {self.product.name} ({option_name})"

    def total_price(self):
        price = self.product.price
        if self.option and hasattr(self.option, 'price'):
            price = self.option.price
        return price * self.quantity

    def carbon_reduction(self):
        carbon = getattr(self.product, 'carbon_reduction', 0)
        return carbon * self.quantity