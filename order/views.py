from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.views import get_cart
from .models import Address, Order, OrderItem
from django.contrib import messages
from pypromptpay import qr_code
import qrcode
from django.core.files.base import ContentFile
from io import BytesIO
from django.conf import settings
import os

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
            address = get_object_or_404(Address, id=address_id, user=request.user)
        else:
            if not all([full_name, province, district, sub_district, postal_code, address_detail, phone_number]):
                messages.error(request, "กรุณากรอกข้อมูลที่อยู่ให้ครบถ้วน")
                return render(request, 'order/checkout.html', {
                    'cart': cart,
                    'addresses': addresses,
                })
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
                is_default=not addresses.exists()
            )

        # สร้างคำสั่งซื้อ
        order = Order.objects.create(
            user=request.user,
            cart=cart,
            address=address,
            total_price=cart.total_price(),
            total_carbon_reduction=cart.total_carbon_reduction(),
            promptpay_id=settings.PROMPTPAY_ID,
            payment_status='PENDING',
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

        # สร้าง QR Code สำหรับ PromptPay
        try:
            # ใช้ฟังก์ชัน qr_code จาก pypromptpay
            payload = qr_code(
                account=settings.PROMPTPAY_ID,
                one_time=True,
                country="TH",
                money=str(order.total_price),  # แปลงเป็น string ตามเอกสาร
                currency="THB"
            )
            # สร้าง QR Code จาก payload
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(payload)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # บันทึก QR Code
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            file_name = f"order_{order.id}_qrcode.png"
            order.qr_code.save(file_name, ContentFile(buffer.getvalue()))
            order.save()
        except Exception as e:
            messages.error(request, f"ไม่สามารถสร้าง QR Code ได้: {str(e)}")
            return redirect('cart:view_cart')

        # ล้างตะกร้า
        cart.items.all().delete()
        messages.success(request, "สั่งซื้อสำเร็จ! กรุณาชำระเงินโดยสแกน QR Code")
        return redirect('order:payment', order_id=order.id)

    return render(request, 'order/checkout.html', {
        'cart': cart,
        'addresses': addresses,
    })

@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order/payment.html', {'order': order})

@login_required
def order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order/status.html', {'order': order})

@login_required
def confirm_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        # จำลองการยืนยันการชำระเงิน (แทนด้วย API ในอนาคต)
        order.payment_status = 'COMPLETED'
        order.status = 'PROCESSING'
        order.save()
        messages.success(request, "ยืนยันการชำระเงินเรียบร้อยแล้ว")
        return redirect('order:order_status', order_id=order.id)
    return redirect('order:order_status', order_id=order.id)