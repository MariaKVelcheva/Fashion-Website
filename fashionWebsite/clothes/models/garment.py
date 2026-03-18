from django.db import models
from django.utils.text import slugify


class Garment(models.Model):
    category = models.ForeignKey(
        to="clothes.Category",
        on_delete=models.CASCADE,
        related_name='garments',
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

    color = models.ForeignKey(
        to="clothes.Color",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='garments',
    )

    size = models.ForeignKey(
        to="clothes.Size",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='garments',
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    @property
    def discount_price(self):
        promotion = self.promotions.filter(is_active=True).first()
        if promotion:
            discount = 0.01 * promotion.discount_percent * self.price
            return self.price - discount
        return self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.category}")
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

