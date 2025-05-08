# cart/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from shopapp.models import Product, ProductOption
from django.contrib.auth.decorators import login_required

@login_required
def view_cart(request):
    # เช็คว่าผู้ใช้มีตะกร้าหรือยัง ถ้าไม่มีให้สร้างใหม่
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/view_cart.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # รับ option_id (ถ้ามี) และจำนวนสินค้า
    option_id = request.POST.get('option_id')
    option = ProductOption.objects.get(id=option_id) if option_id else None
    quantity = int(request.POST.get('quantity', 1))

    # หา cart ของ user หรือสร้างใหม่
    cart, created = Cart.objects.get_or_create(user=request.user)

    # เช็คว่ามีสินค้าใน cart นี้แล้วหรือยัง ถ้ามีเพิ่มจำนวน ถ้าไม่มีให้สร้างใหม่
    item, created = CartItem.objects.get_or_create(cart=cart, product=product, option=option)
    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()

    return redirect('view_cart')

@login_required
def remove_from_cart(request, item_id):
    try:
        item = CartItem.objects.get(id=item_id)
        item.delete()  # ลบไอเท็มจากตะกร้า
    except CartItem.DoesNotExist:
        pass  # ถ้าไอเท็มไม่พบ จะไม่ทำอะไร

    return redirect('cart:view_cart')  # ส่งกลับไปที่หน้า "view_cart"