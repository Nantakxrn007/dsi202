# cart/context_processors.py

from .models import CartItem, Cart
from django.db.models import Sum

def cart_item_count(request):
    count = 0
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            session_key = request.session.session_key
            if session_key:
                cart = Cart.objects.filter(session_key=session_key, user__isnull=True).first()
            else:
                cart = None

        if cart:
            count = CartItem.objects.filter(cart=cart).aggregate(Sum('quantity'))['quantity__sum'] or 0
    except:
        pass

    return {'cart_item_count': count}
