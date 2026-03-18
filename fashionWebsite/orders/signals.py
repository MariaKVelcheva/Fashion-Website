from django.dispatch import receiver
from django.db.models.signals import post_save
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
        for item in instance.items.all():
            item.garment.stock += item.quantity
            item.garment.save(update_fields=['stock'])

        Order.objects.filter(pk=instance.pk).update(status='cancelled')