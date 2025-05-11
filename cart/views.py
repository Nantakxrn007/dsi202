from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Cart, CartItem
from shopapp.models import Product, ProductOption

def get_cart(request):
    """ดึงหรือสร้างตะกร้าสำหรับผู้ใช้หรือ guest"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        # ถ้ามี session cart ให้โอนสินค้า
        session_key = request.session.get('cart_session_key')
        if session_key:
            try:
                session_cart = Cart.objects.get(session_key=session_key, user__isnull=True)
                for session_item in session_cart.items.all():
                    # ลองหา CartItem ที่มีอยู่ในตะกร้าผู้ใช้
                    try:
                        user_item = CartItem.objects.get(
                            cart=cart,
                            product=session_item.product,
                            option=session_item.option
                        )
                        user_item.quantity += session_item.quantity
                        user_item.save()
                    except CartItem.DoesNotExist:
                        session_item.cart = cart
                        session_item.save()
                session_cart.delete()  # ลบ session cart
                request.session.pop('cart_session_key', None)  # แก้จาก semssion เป็น session
            except Cart.DoesNotExist:
                pass
        return cart
    else:
        # ใช้ session สำหรับ guest
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key, user__isnull=True)
        request.session['cart_session_key'] = session_key
        return cart

def view_cart(request):
    cart = get_cart(request)
    return render(request, 'cart/view_cart.html', {'cart': cart})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method != 'POST':
        return redirect('shopapp:product_detail', product_id=product_id)

    option_id = request.POST.get('option_id')
    quantity = int(request.POST.get('quantity', 1))
    option = ProductOption.objects.get(id=option_id) if option_id else None

    cart = get_cart(request)

    try:
        item = CartItem.objects.get(cart=cart, product=product, option=option)
        item.quantity += quantity
        item.save()
    except CartItem.DoesNotExist:
        CartItem.objects.create(
            cart=cart,
            product=product,
            option=option,
            quantity=quantity
        )
    except CartItem.MultipleObjectsReturned:
        items = CartItem.objects.filter(cart=cart, product=product, option=option)
        total_quantity = sum(item.quantity for item in items) + quantity
        items.exclude(id=items.first().id).delete()
        item = items.first()
        item.quantity = total_quantity
        item.save()

    if not request.user.is_authenticated:
        # เก็บ URL ก่อนไป login
        request.session['next'] = request.get_full_path()
        return redirect('login')
    return redirect('cart:view_cart')

@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        try:
            item = CartItem.objects.get(id=item_id, cart__user=request.user)
            item.delete()
        except CartItem.DoesNotExist:
            pass
    return redirect('cart:view_cart')

@login_required
def update_cart_item(request, item_id):
    if request.method == 'POST':
        try:
            item = CartItem.objects.get(id=item_id, cart__user=request.user)
            quantity = int(request.POST.get('quantity', item.quantity))
            option_id = request.POST.get('option_id')
            option = ProductOption.objects.get(id=option_id) if option_id else None

            if quantity > 0:
                if option != item.option:
                    try:
                        existing_item = CartItem.objects.get(cart=item.cart, product=item.product, option=option)
                        existing_item.quantity += quantity
                        existing_item.save()
                        item.delete()
                    except CartItem.DoesNotExist:
                        item.option = option
                        item.quantity = quantity
                        item.save()
                else:
                    item.quantity = quantity
                    item.save()
            else:
                item.delete()
        except (CartItem.DoesNotExist, ProductOption.DoesNotExist):
            pass
    return redirect('cart:view_cart')



@login_required
def checkout(request):
    cart = get_cart(request)
    return render(request, 'cart/checkout.html', {'cart': cart})