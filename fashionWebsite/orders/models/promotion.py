from django.db import models
from django.utils import timezone


class Promotion(models.Model):
    CHOICES = (
        ("code", "Promo code"),
        ("garment", "Garment Discount"),
        ("category", "Category"),
        ("order", "Order Discount"),
    )

    code = models.CharField(
        max_length=10,
    )

    type = models.CharField(
        max_length=20,
        choices=CHOICES,
    )

    discount_percent = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    valid_from = models.DateTimeField()

    valid_until = models.DateTimeField()

    garments = models.ForeignKey(
        to="clothes.Garment",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="promotions",
    )

    categories = models.ManyToManyField(
        to="clothes.Category",
        blank=True,
        null=True,
        related_name="promotions",
    )

    @property
    def is_active(self):
        now = timezone.now()
        return self.valid_from <= now <= self.valid_until

    def __str__(self):
        return self.code
