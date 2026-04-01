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

    @property
    def main_image(self):
        return self.images.first()

    def get_available_colors(self):
        return list({p.color for p in self.products.select_related("color")})

    def get_available_sizes(self):
        return list({p.size for p in self.products.select_related("size")})

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(f"{self.name}-{self.category}")
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

