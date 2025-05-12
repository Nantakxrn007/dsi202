from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.views import get_cart  # Import get_cart จาก cart/views.py
from .models import Address, Order, OrderItem
from django.contrib import messages

@login_required
def checkout(request):
    cart = get_cart(request)
    if not cart.items.exists():
        messages.error(request, "ตะกร้าสินค้าของคุณว่างเปล่า")
        return redirect('cart:view_cart')

    addresses = Address.objects.filter(user=request.user)

    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        full_name = request.POST.get('full_name')
        province = request.POST.get('province')
        district = request.POST.get('district')
        sub_district = request.POST.get('sub_district')
        postal_code = request.POST.get('postal_code')
        address_detail = request.POST.get('address_detail')
        note = request.POST.get('note', '')
        phone_number = request.POST.get('phone_number')

        if address_id:
            # ใช้ที่อยู่ที่มีอยู่
            address = get_object_or_404(Address, id=address_id, user=request.user)
        else:
            # ตรวจสอบว่ากรอกข้อมูลที่อยู่ใหม่ครบหรือไม่ (ยกเว้น note)
            if not all([full_name, province, district, sub_district, postal_code, address_detail, phone_number]):
                messages.error(request, "กรุณากรอกข้อมูลที่อยู่ให้ครบถ้วน")
                return render(request, 'order/checkout.html', {
                    'cart': cart,
                    'addresses': addresses,
                })
            # สร้างที่อยู่ใหม่
            address = Address.objects.create(
                user=request.user,
                full_name=full_name,
                province=province,
                district=district,
                sub_district=sub_district,
                postal_code=postal_code,
                address_detail=address_detail,
                note=note,
                phone_number=phone_number,
                is_default=not addresses.exists()  # ตั้งเป็น default ถ้าไม่มีที่อยู่อื่น
            )

        # สร้างคำสั่งซื้อ
        order = Order.objects.create(
            user=request.user,
            cart=cart,
            address=address,
            total_price=cart.total_price(),
            total_carbon_reduction=cart.total_carbon_reduction(),
        )

        # สร้าง OrderItems จาก CartItems
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                option=item.option,
                quantity=item.quantity,
                price=item.total_price() / item.quantity,
            )

        # ล้างตะกร้า
        cart.items.all().delete()
        messages.success(request, "สั่งซื้อสำเร็จ!")
        return redirect('order:order_confirmation', order_id=order.id)

    return render(request, 'order/checkout.html', {
        'cart': cart,
        'addresses': addresses,
    })

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order/order_confirmation.html', {'order': order})