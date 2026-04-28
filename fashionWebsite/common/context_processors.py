from django.db.models import F
from django.utils import timezone

from fashionWebsite.clothes.models import Category, Color, Size
from fashionWebsite.orders.models import Order
from fashionWebsite.promotions.models import Promotion


def global_filters(request):
    now = timezone.now()

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

    promo_categories = Promotion.objects.filter(
        type="category",
        valid_from__lte=now,
        valid_until__gte=now,
    ).exclude(
        max_uses__isnull=False,
        times_used__gte=F("max_uses"),
    )

    return {
        'categories': Category.objects.all(),
        'colors': Color.objects.all(),
        'sizes': Size.objects.all(),
        'cart_count': cart_count,
        "promo_categories": promo_categories,
    }

