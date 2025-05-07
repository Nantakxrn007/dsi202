def cart_quantity(request):
    cart = request.session.get('cart', {})
    total_quantity = sum(item['quantity'] for item in cart.values())
    return {'cart_quantity': total_quantity}