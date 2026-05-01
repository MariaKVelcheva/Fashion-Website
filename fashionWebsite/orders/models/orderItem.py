from django.db import models
from django.utils.translation import gettext_lazy as _


class OrderItem(models.Model):
    order = models.ForeignKey(
        to="orders.Order",
        on_delete=models.CASCADE,
        verbose_name=_("Order"),
        related_name='items',
    )

    product = models.ForeignKey(
        to="clothes.Product",
        on_delete=models.PROTECT,
        verbose_name=_("Product"),
        related_name='items',
    )

    quantity = models.PositiveIntegerField(
        verbose_name=_("Quantity"),
    )

    unit_price = models.DecimalField(
        verbose_name=_("Unit Price"),
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["order", "product"],
                name="unique_order_product"
            )
        ]
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    @property
    def line_total(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return self.product.garment.name

