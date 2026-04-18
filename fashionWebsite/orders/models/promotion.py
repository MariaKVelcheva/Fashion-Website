from django.db import models
from django.utils import timezone


class Promotion(models.Model):
    CHOICES = (
        ("code", "Promo code"),
        ("garment", "Garment Discount"),
        ("category", "Category Discount"),
        ("order", "Order Discount"),
    )

    code = models.CharField(max_length=20, unique=True)

    type = models.CharField(
        max_length=20,
        choices=CHOICES,
        default="code",
    )

    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)

    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()

    min_order_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    max_uses = models.PositiveIntegerField(null=True, blank=True)
    times_used = models.PositiveIntegerField(default=0)

    garments = models.ManyToManyField(
        to="clothes.Garment",
        blank=True,
        related_name="promotions",
    )

    categories = models.ManyToManyField(
        to="clothes.Category",
        blank=True,
        related_name="promotions",
    )

    @property
    def is_active(self):
        return self.valid_from <= timezone.now() <= self.valid_until

    @property
    def is_exhausted(self):
        if self.max_uses is None:
            return False
        return self.times_used >= self.max_uses

    @property
    def is_valid(self):
        return self.is_active and not self.is_exhausted

    def apply_to_order(self, order):
        """Returns the discounted total for a given order."""
        discount = order.total_amount * (self.discount_percent / 100)
        return max(order.total_amount - discount, 0)

    def __str__(self):
        return f"{self.code} ({self.discount_percent}%)"