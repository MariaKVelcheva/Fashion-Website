from django.db import models


class OrderItem(models.Model):
    order = models.ForeignKey(
        to="orders.Order",
        on_delete=models.CASCADE,
        related_name='items',
    )

    product = models.ForeignKey(
        to="clothes.Product",
        on_delete=models.PROTECT,
        related_name='items',
    )

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(
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

    @property
    def line_total(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return self.product.garment.name

