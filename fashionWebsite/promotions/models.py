from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Promotion(models.Model):
    CHOICES = (
        ("code", _("Promo code")),
        ("garment", _("Garment Discount")),
        ("category", _("Category Discount")),
        ("order", _("Order Discount")),
    )

    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_("Code"),
    )

    type = models.CharField(
        max_length=20,
        choices=CHOICES,
        default="code",
        verbose_name=_("Promo Type"),
    )

    discount_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Discount Percent"),
    )

    valid_from = models.DateTimeField(
        verbose_name=_("Valid From"),
    )

    valid_until = models.DateTimeField(
        verbose_name=_("Valid Until"),
    )

    min_order_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Minimum Order Amount"),
    )

    max_uses = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Maximum Uses"),
    )

    times_used = models.PositiveIntegerField(
        verbose_name=_("Times Used"),
        default=0
    )

    garments = models.ManyToManyField(
        to="clothes.Garment",
        blank=True,
        related_name="promotions",
        verbose_name=_("Garments"),
    )

    categories = models.ManyToManyField(
        to="clothes.Category",
        blank=True,
        related_name="promotions",
        verbose_name=_("Categories"),
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
        discount = order.total_amount * (self.discount_percent / 100)
        return max(order.total_amount - discount, 0)

    class Meta:
        verbose_name = _("Promotion")
        verbose_name_plural = _("Promotions")

    def __str__(self):
        return f"{self.code} ({self.discount_percent}%)"