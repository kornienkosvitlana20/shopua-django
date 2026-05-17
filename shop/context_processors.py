from .models import Cart


def cart_count(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            return {'cart_item_count': cart.get_total_items()}
        except Cart.DoesNotExist:
            pass
    return {'cart_item_count': 0}
