from django.urls import path
from .views import HomePageView, ProductDetailView , FirstPageView

urlpatterns = [
    path('', FirstPageView.as_view(), name='first'),  # หน้าหลัก เริ่มที่ first
    path('home/', HomePageView.as_view(), name='home'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]