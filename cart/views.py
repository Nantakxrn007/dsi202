# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.views import View
from django.http import JsonResponse
from shopapp.models import Product, ProductOption

def get_cart_key(request):
    # ถ้า user login แล้วจะใช้ key ที่แตกต่างกัน
    if request.user.is_authenticated:
        return f'cart_user_{request.user.id}'
    return 'cart'  # ถ้า guest จะใช้ cart ทั่วไป

def get_cart(request):
    cart_key = get_cart_key(request)
    return request.session.get(cart_key, {})

def save_cart(request, cart):
    cart_key = get_cart_key(request)
    request.session[cart_key] = cart
    request.session['cart'] = cart  # สำหรับ context processor
    request.session.modified = True  # ✅ บอก Django ว่า session มีการเปลี่ยนแปลง

def merge_cart_on_login(request, user):
    # Merge ตะกร้าของ guest กับ user เมื่อ login
    guest_cart = request.session.get('cart', {})
    user_key = f'cart_user_{user.id}'
    user_cart = request.session.get(user_key, {})

    # รวม cart ถ้าหาก key ซ้ำกัน จะรวมจำนวนสินค้า
    for key, item in guest_cart.items():
        if key in user_cart:
            user_cart[key]['quantity'] += item['quantity']
        else:
            user_cart[key] = item

    # บันทึกลงใน session
    request.session[user_key] = user_cart
    request.session['cart'] = user_cart  # อัปเดต context processor ด้วย
    save_cart(request, user_cart)

# เมื่อผู้ใช้ login ระบบจะ merge ข้อมูลตะกร้าของ guest เข้ากับ user
@receiver(user_logged_in)
def on_user_login(sender, request, user, **kwargs):
    merge_cart_on_login(request, user)

class CartAddView(View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        option_id = request.POST.get('option')
        quantity = int(request.POST.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)
        option = get_object_or_404(ProductOption, id=option_id) if option_id else None

        cart = get_cart(request)

        key = f"{product_id}:{option_id or 'none'}"

        if key in cart:
            cart[key]['quantity'] += quantity
        else:
            cart[key] = {
                'product_id': product.id,
                'option_id': option.id if option else None,
                'product_name': product.name,
                'option_name': option.name if option else 'ไม่มี',
                'quantity': quantity,
                'price': float(product.price),
                'carbon_reduction': float(product.carbon_reduction),
                'image_url': product.image.url if product.image else '',
            }

        save_cart(request, cart)
        total_quantity = sum(item['quantity'] for item in cart.values())

        # ส่งข้อมูลเป็น JSON
        return JsonResponse({
            "success": True,
            "cart_quantity": total_quantity,
        })

class CartDetailView(View):
    def get(self, request):
        cart = get_cart(request)
        cart_items = []
        cart_total = 0
        carbon_total = 0

        for item in cart.values():
            item_total = item['price'] * item['quantity']
            cart_total += item_total
            carbon_total += item['carbon_reduction'] * item['quantity']
            cart_items.append({
                'product_name': item['product_name'],
                'option_name': item['option_name'],
                'quantity': item['quantity'],
                'price': item['price'],
                'total_price': item_total,
                'carbon_reduction': item['carbon_reduction'],
                'product_id': item['product_id'],
                'option_id': item['option_id'],
                'image_url': item['image_url'],
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
        cart = get_cart(request)

        if key in cart:
            del cart[key]
            save_cart(request, cart)

        return redirect('cart:cart_detail')

class CartClearView(View):
    def post(self, request):
        save_cart(request, {})  # clear cart
        return redirect('cart:cart_detail')
