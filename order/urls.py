from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('confirm-payment/<int:order_id>/', views.confirm_payment, name='confirm_payment'),
    path('status/', views.order_status, name='order_status'),
    path('detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('delivered/', views.delivered_orders, name='delivered_orders'),
]