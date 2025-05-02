from django.views.generic import ListView, DetailView
from .models import Product
from django.db.models import Q  # สำหรับค้นหาแบบ flexible
from django.views.generic import TemplateView 


class HomePageView(ListView):
    model = Product                   # จะใช้ model นี้อัตโนมัติ
    template_name = 'home.html'       # ชื่อ template ที่จะเรนเดอร์
    context_object_name = 'products'  # ชื่อของตัวแปรที่ใช้ใน template

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Product.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
        return Product.objects.all()
    
class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

class FirstPageView(TemplateView):
    template_name = 'first.html'
