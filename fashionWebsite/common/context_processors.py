from fashionWebsite.clothes.models import Category, Color, Size
from fashionWebsite.orders.models import Order


def global_filters(request):
    cart_count = 0
    if request.user.is_authenticated:
        order = Order.objects.filter(
            customer=request.user,
            status="pending"
        ).first()
        if order:
            cart_count = sum(i.quantity for i in order.items.all())
    else:
        cart = request.session.get("cart", {})
        cart_count = sum(cart.values())

    return {
        'categories': Category.objects.all(),
        'colors': Color.objects.all(),
        'sizes': Size.objects.all(),
        'cart_count': cart_count,
    }

