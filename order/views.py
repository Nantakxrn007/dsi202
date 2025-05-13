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

        # Create order
        order = Order.objects.create(
            user=request.user,
            cart=cart,
            address=address,
            total_price=cart.total_price(),
            total_carbon_reduction=cart.total_carbon_reduction(),
            promptpay_id=settings.PROMPTPAY_ID,
            status='PENDING',
            payment_status='PENDING',
        )

        # Create OrderItems from CartItems
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                option=item.option,
                quantity=item.quantity,
                price=item.total_price() / item.quantity,
            )

        # Generate QR Code for PromptPay
        try:
            payload = qr_code(
                account=settings.PROMPTPAY_ID,
                one_time=True,
                country="TH",
                money=str(order.total_price),
                currency="THB"
            )
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(payload)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            buffer = BytesIO()
            img.save(buffer, format="PNG")
            file_name = f"order_{order.id}_qrcode.png"
            order.qr_code.save(file_name, ContentFile(buffer.getvalue()))
            order.save()
        except Exception as e:
            messages.error(request, f"ไม่สามารถสร้าง QR Code ได้: {str(e)}")
            order.delete()  # Delete the order if QR code generation fails
            return redirect('cart:view_cart')

        # Clear cart
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
    # Ensure order is in PENDING status
    if order.status != 'PENDING' or order.payment_status != 'PENDING':
        order.status = 'PENDING'
        order.payment_status = 'PENDING'
        order.save()
    return render(request, 'order/payment.html', {'order': order})



@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order/order_detail.html', {'order': order})


@login_required
def order_status(request):
    filter_param = request.GET.get('filter', 'all')
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    if filter_param == 'unpaid':
        orders = orders.filter(status='PENDING', payment_status='PENDING')
    elif filter_param == 'shipping':
        orders = orders.filter(status__in=['PROCESSING', 'SHIPPED'], payment_status='COMPLETED')
    elif filter_param == 'delivered':
        orders = orders.filter(status='DELIVERED')

    return render(request, 'order/order_status.html', {
        'orders': orders,
        'filter': filter_param
    })

@login_required
def confirm_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        order.payment_status = 'COMPLETED'
        order.status = 'PROCESSING'
        order.save()
        messages.success(request, "ยืนยันการชำระเงินเรียบร้อยแล้ว")
        return redirect('order:order_status')
    return redirect('order:payment', order_id=order.id)

@login_required
def delivered_orders(request):
    delivered_orders = Order.objects.filter(user=request.user, status='DELIVERED').order_by('-created_at')
    return render(request, 'order/delivered_orders.html', {'delivered_orders': delivered_orders})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == 'PENDING' and order.payment_status == 'PENDING':
        order.status = 'CANCELLED'
        order.save()
        messages.success(request, f"ยกเลิกคำสั่งซื้อ #{order.id} เรียบร้อยแล้ว")
    else:
        messages.error(request, "ไม่สามารถยกเลิกคำสั่งซื้อนี้ได้")
    return redirect('order:order_status')