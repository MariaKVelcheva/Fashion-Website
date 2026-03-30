from decimal import Decimal

from django.db import models
from django.utils.text import slugify


class Garment(models.Model):
    category = models.ForeignKey(
        to="clothes.Category",
        on_delete=models.CASCADE,
        related_name='garments',
        default="",
        null=True,
        blank=True,
    )

    name = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
    )

    profile_image = models.URLField(
        null=True,
        blank=True,
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    @property
    def is_available(self):
        return self.products.filter(stock__gt=0).exists()

    def get_available_sizes(self):
        return self.products.values_list("size__name", flat=True).distinct()

    def get_available_colors(self):
        return self.products.values_list("color__name", flat=True).distinct()

    @property
    def discount_price(self):
        if self.promotion and self.promotion.is_active:
            discount = (0.01 * float(self.promotion.discount_percent) * float(self.price))
            return self.price - Decimal(discount)
        return self.price

    @property
    def has_discount(self):
        return self.discount_price < self.price

    @property
    def display_price(self):
        return self.discount_price if self.has_discount else self.price

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(f"{self.name}-{self.category}")
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

