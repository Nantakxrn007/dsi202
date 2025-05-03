from django.views.generic import ListView, DetailView, TemplateView
from .models import Product
from django.db.models import Q  # สำหรับค้นหาแบบ flexible

class HomePageView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q')

        # ดึงสินค้าที่เป็น Flash Sale ก่อน
        flash_sale_products = Product.objects.filter(sale_informations__is_on_sale=True).distinct()
        flash_sale_ids = flash_sale_products.values_list('id', flat=True)

        if query:
            return Product.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            ).exclude(id__in=flash_sale_ids)

        return Product.objects.exclude(id__in=flash_sale_ids)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ส่ง flash_sale_products ไปยัง template
        context['flash_sale_products'] = Product.objects.filter(sale_informations__is_on_sale=True).distinct()
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

class FirstPageView(TemplateView):
    template_name = 'first.html'