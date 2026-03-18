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

    image = models.URLField(
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

    color = models.ManyToManyField(
        to="clothes.Color",
        related_name='garments',
    )

    size = models.ManyToManyField(
        to="clothes.Size",
        related_name='garments',
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    stock = models.IntegerField(
        default=1,
    )

    @property
    def is_available(self):
        return self.stock > 0

    @property
    def discount_price(self):
        promotion = self.promotions.filter(is_active=True).first()
        if promotion:
            discount = 0.01 * promotion.discount_percent * self.price
            return self.price - discount
        return self.price

    @property
    def has_discount(self):
        return self.discount_price < self.price

    @property
    def display_price(self):
        return self.discount_price if self.has_discount else self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.category}")
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

