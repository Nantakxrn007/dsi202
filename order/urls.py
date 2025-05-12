from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('status/<int:order_id>/', views.order_status, name='order_status'),
    path('confirm-payment/<int:order_id>/', views.confirm_payment, name='confirm_payment'),
]