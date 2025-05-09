from django.urls import path , include
from .views import HomePageView, ProductDetailView , FirstPageView
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', FirstPageView.as_view(), name='first'),  # หน้าหลัก เริ่มที่ first
    path('home/', HomePageView.as_view(), name='home'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('profile/', views.user_profile, name='user_profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('cart/', include('cart.urls', namespace='cart')),  # เพิ่ม namespace='cart' ตรงนี้
]