# cart/urls.py
from django.urls import path
from .views import CartAddView, CartDetailView , CartRemoveView , CartClearView

app_name = 'cart'

urlpatterns = [
    path('add/', CartAddView.as_view(), name='cart_add'),
    path('', CartDetailView.as_view(), name='cart_detail'),
    path('remove/', CartRemoveView.as_view(), name='cart_remove'),  # ← เพิ่มบรรทัดนี้
    path('clear/', CartClearView.as_view(), name='cart_clear'),  # ← เพิ่มบรรทัดนี้



]