# cart/signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

@receiver(user_logged_in)
def merge_cart_on_login(sender, request, user, **kwargs):
    guest_cart = request.session.get('cart', {})
    user_key = f'cart_user_{user.id}'
    user_cart = request.session.get(user_key, {})

    # รวม cart
    for key, item in guest_cart.items():
        if key in user_cart:
            user_cart[key]['quantity'] += item['quantity']
        else:
            user_cart[key] = item

    # เก็บลง session
    request.session[user_key] = user_cart
    request.session['cart'] = user_cart  # อัปเดต context processor ด้วย
