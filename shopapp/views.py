from django.views.generic import ListView, DetailView, TemplateView
from .models import Product
from django.db.models import Q  # สำหรับค้นหาแบบ flexible

class HomePageView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Product.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Use the related_name 'sale_informations' to filter
        flash_sale_products = Product.objects.filter(sale_informations__is_on_sale=True).distinct()
        context['flash_sale_products'] = flash_sale_products
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

class FirstPageView(TemplateView):
    template_name = 'first.html'