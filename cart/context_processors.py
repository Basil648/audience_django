from .models import Cart

def cart_context(request):
    total = 0
    items = []

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            items = cart.cart_items.select_related('product').all()
            total = sum(item.total_price for item in items)
        except Cart.DoesNotExist:
            pass

    return {
        'cart_total': total,
        'cart_items': items,
    }
