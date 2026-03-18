from django.db import models


class OrderItem(models.Model):
    order = models.ForeignKey(
        to="orders.Order",
        on_delete=models.CASCADE,
        related_name='items',
    )

    garment = models.ForeignKey(
        to="clothes.Garment",
        on_delete=models.PROTECT,
        related_name='items',
    )

    quantity = models.PositiveIntegerField()

    promotion = models.ForeignKey(
        to="orders.Promotion",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    @property
    def line_total(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return self.garment.name

