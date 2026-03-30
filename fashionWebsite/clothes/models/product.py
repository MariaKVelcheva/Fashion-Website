from django.db import models


class Product(models.Model):
    garment = models.ForeignKey(
        to="clothes.Garment",
        on_delete=models.CASCADE,
        related_name="products"
    )

    size = models.ForeignKey(
        to="clothes.Size",
        on_delete=models.CASCADE,
        related_name="products"
    )

    color = models.ForeignKey(
        to="clothes.Color",
        on_delete=models.CASCADE,
        related_name="products"
    )

    stock = models.PositiveIntegerField(default=0)

    sku = models.CharField(max_length=50, unique=True, blank=True)

    class Meta:
        unique_together = ("garment", "size", "color")
        indexes = [
            models.Index(fields=["garment", "size", "color"]),
        ]

    def __str__(self):
        return f"{self.garment.name} - {self.size.name} - {self.color.name}"