from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from fashionWebsite.common.tasks import send_email_task
from fashionWebsite.orders.models import OrderItem, Order


@receiver(post_save, sender=OrderItem)
def update_stock(sender, instance, created, **kwargs):
    if created and instance.order.status in ["paid", "shipped"]:
        garment = instance.garment
        garment.stock -= instance.quantity
        garment.save(update_fields=['stock'])


@receiver(post_save, sender=Order)
def restore_stock(sender, instance, **kwargs):
    if instance.status == "cancelled":
        items = instance.items.select_related("product__garment").all()
        for item in items:
            item.product.garment.stock += item.quantity
            item.product.garment.save(update_fields=['stock'])


@receiver(post_save, sender=Order)
def send_shipping_confirmation(sender, instance, created, **kwargs):
    if not created:
        if instance._original_status != "shipped" and instance.status == "shipped":
            send_email_task.delay(
                subject=_("Your order has been shipped!"),
                template_name="emails/shipping_confirmation.html",
                context={
                    "order_id": instance.id,
                },
                recipient_list=[instance.customer.email],
            )


@receiver(post_save, sender=Order)
def send_order_confirmation(sender, instance, created, **kwargs):
    if not instance.customer or not instance.customer.email:
        return

    if instance.status == "confirmed":
        items_raw = OrderItem.objects.select_related("product__garment",
                                                     "product__color", "product__size").filter(order=instance)
        items = []

        for item in items_raw:
            name = item.product.garment.name
            size = item.product.size.name
            color = item.product.color.name
            unit_price = float(item.unit_price)
            quantity = item.quantity
            line_total = float(unit_price * quantity)
            items.append({"name": name, "size": size, "color": color,
                          "quantity": quantity, "line_total": line_total})

        context = {
            "order_id": instance.id,
            "customer_name": instance.customer.customer.full_name,
            "user_email": instance.customer.email,
            "shipping_address": instance.shipping_address,
            "phone_number": instance.phone_number,
            "payment_type": instance.payment_type,
            "items": items,
            "total_amount": float(instance.total_amount),

        }

        send_email_task.delay(
            subject="New order placed",
            template_name="emails/order_placed.html",
            context=context,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
        )
