from datetime import timedelta
from decimal import Decimal

from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Garment(models.Model):
    category = models.ManyToManyField(
        to="clothes.Category",
        related_name='garments',
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

    main_image = models.ImageField(
        upload_to='garments/',
        blank=True,
        null=True,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,)

    @property
    def is_new(self):
        return timezone.now() - self.created_at < timedelta(days=60)

    @property
    def is_available(self):
        return self.products.filter(stock__gt=0).exists()

    def get_available_colors(self):
        return list({p.color for p in self.products.select_related("color")})

    def get_available_sizes(self):
        return list({p.size for p in self.products.select_related("size")})

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

