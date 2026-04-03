from fashionWebsite.orders.models import Order


def get_or_create_cart(user):
    order = Order.objects.filter(
        customer=user,
        status="pending"
    ).first()

    if not order:
        order = Order.objects.create(
            customer=user,
            status="pending",
            total_amount=0
        )

    return order


def update_order_total(order):
    total = sum(item.line_total for item in order.items.all())
    order.total_amount = total
    order.save()

