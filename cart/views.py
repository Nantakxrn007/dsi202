# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from shopapp.models import Product, ProductOption
from django.views import View

class CartAddView(View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        option_id = request.POST.get('option')
        quantity = int(request.POST.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)
        option = get_object_or_404(ProductOption, id=option_id) if option_id else None

        cart = request.session.get('cart', {})

        key = f"{product_id}:{option_id or 'none'}"

        if key in cart:
            cart[key]['quantity'] += quantity
        else:
            cart[key] = {
                'product_id': product.id,
                'option_id': option.id if option else None,
                'product_name': product.name,
                'option_name': option.name if option else 'ไม่มี',  # แก้ไขตรงนี้
                'quantity': quantity,
                'price': float(product.price),
                'carbon_reduction': float(product.carbon_reduction),
            }

        request.session['cart'] = cart
        return redirect('cart:cart_detail')


class CartDetailView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        cart_items = []
        cart_total = 0
        carbon_total = 0

        for item in cart.values():
            item_total = item['price'] * item['quantity']
            cart_total += item_total
            carbon_total += item['carbon_reduction'] * item['quantity']
            cart_items.append({
                'product_name': item['product_name'],
                'option_name': item['option_name'],  # ถ้ามีจะให้แสดงตัวเลือก
                'quantity': item['quantity'],
                'price': item['price'],
                'total_price': item_total,
                'carbon_reduction': item['carbon_reduction'],
                'product_id': item['product_id'],     # ← เพิ่ม
                'option_id': item['option_id'],       # ← เพิ่ม
            })

        context = {
            'cart_items': cart_items,
            'cart_total': cart_total,
            'carbon_total': carbon_total,
        }
        return render(request, 'cart/cart_detail.html', context)
    



class CartRemoveView(View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        option_id = request.POST.get('option_id')

        key = f"{product_id}:{option_id or 'none'}"
        cart = request.session.get('cart', {})

        if key in cart:
            del cart[key]
            request.session['cart'] = cart

        return redirect('cart:cart_detail')
    
class CartClearView(View):
    def post(self, request):
        request.session['cart'] = {}
        return redirect('cart:cart_detail')