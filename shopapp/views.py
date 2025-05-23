# shopapp/views.py
from django.views.generic import ListView, DetailView, TemplateView
from .models import Product
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.views.decorators.csrf import csrf_exempt
from cart.views import get_cart
from order.models import Order
from django.contrib import messages
from .models import Profile

class HomePageView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q')
        category = self.request.GET.get('category')

        # Get flash sale products first
        flash_sale_products = Product.objects.filter(sale_informations__is_on_sale=True).distinct()
        flash_sale_ids = flash_sale_products.values_list('id', flat=True)

        queryset = Product.objects.exclude(id__in=flash_sale_ids)

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
        
        if category:
            queryset = queryset.filter(category=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flash_sale_products'] = Product.objects.filter(sale_informations__is_on_sale=True).distinct()
        context['categories'] = Product.CATEGORY_CHOICES  # Send categories to template
        context['selected_category'] = self.request.GET.get('category', '')  # Current selected category
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

class FirstPageView(TemplateView):
    template_name = 'first.html'

@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data.get('email')
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            get_cart(request)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})


@login_required
def user_profile(request):
    unpaid_count = Order.objects.filter(
        user=request.user, status='PENDING', payment_status='PENDING'
    ).count()
    shipping_count = Order.objects.filter(
        user=request.user, status__in=['PROCESSING', 'SHIPPED'], payment_status='COMPLETED'
    ).count()
    delivered_count = Order.objects.filter(
        user=request.user, status='DELIVERED'
    ).count()

    return render(request, 'user_profile.html', {
        'user': request.user,
        'unpaid_count': unpaid_count,
        'shipping_count': shipping_count,
        'delivered_count': delivered_count
    })


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()

        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
            profile.save()

        messages.success(request, "บันทึกการเปลี่ยนแปลงโปรไฟล์เรียบร้อยแล้ว")
        return redirect('profile')

    return render(request, 'edit_profile.html', {
        'user': request.user
    })