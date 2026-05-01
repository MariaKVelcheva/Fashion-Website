from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    garment = models.ForeignKey(
        to="clothes.Garment",
        on_delete=models.CASCADE,
        verbose_name=_("Product"),
        related_name="products"
    )

    size = models.ForeignKey(
        to="clothes.Size",
        on_delete=models.CASCADE,
        verbose_name=_("Size"),
        related_name="products"
    )

    color = models.ForeignKey(
        to="clothes.Color",
        on_delete=models.CASCADE,
        verbose_name=_("Color"),
        related_name="products"
    )

    stock = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        indexes = [
            models.Index(fields=["garment", "size", "color"]),
        ]

    def __str__(self):
        return f"{self.garment.name} - {self.size.name} - {self.color.name}"