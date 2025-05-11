from django.urls import path , include
from .views import HomePageView, ProductDetailView , FirstPageView , signup_view
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
        path('', FirstPageView.as_view(), name='first'),  # หน้าหลัก เริ่มที่ first
        path('home/', HomePageView.as_view(), name='home'),
        path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
        path('profile/', views.user_profile, name='user_profile'),
        path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
        path('cart/', include('cart.urls', namespace='cart')),  # เพิ่ม namespace='cart' ตรงนี้
        path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
        path('signup/', signup_view, name='signup'),
            # เพิ่ม URLs สำหรับการรีเซ็ตรหัสผ่าน
        path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
        path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
        path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
        path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    ]