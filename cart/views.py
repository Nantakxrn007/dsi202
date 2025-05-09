from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from shopapp.models import Product, ProductOption

@login_required
def view_cart(request):
    # ดึงตะกร้าของผู้ใช้หรือสร้างใหม่
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/view_cart.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method != 'POST':
        return redirect('shopapp:product_detail', product_id=product_id)

    # รับ option_id และ quantity จาก POST
    option_id = request.POST.get('option_id')
    quantity = int(request.POST.get('quantity', 1))
    option = ProductOption.objects.get(id=option_id) if option_id else None

    # ดึงหรือสร้างตะกร้าของผู้ใช้
    cart, created = Cart.objects.get_or_create(user=request.user)

    # ลองดึง CartItem ที่มีอยู่ หรือสร้างใหม่
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
        # จัดการกรณีมีข้อมูลซ้ำโดยรวมจำนวนและลบรายการที่ซ้ำ
        items = CartItem.objects.filter(cart=cart, product=product, option=option)
        total_quantity = sum(item.quantity for item in items) + quantity
        items.exclude(id=items.first().id).delete()
        item = items.first()
        item.quantity = total_quantity
        item.save()

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

            # อัปเดตหรือลบรายการ
            if quantity > 0:
                # ตรวจสอบว่าเปลี่ยนตัวเลือกหรือไม่
                if option != item.option:
                    # ลองหา CartItem ที่มีตัวเลือกใหม่
                    try:
                        existing_item = CartItem.objects.get(cart=item.cart, product=item.product, option=option)
                        existing_item.quantity += quantity
                        existing_item.save()
                        item.delete()  # ลบรายการเดิม
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