from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    CHOICES = (
        ("dress", "Dress"),
        ("pants", "Pants"),
        ("skirts", "Skirts"),
        ("shirts", "Shirts"),
        ("jackets", "Jackets"),
        ("cardigans", "Cardigans"),
        ("tops", "Tops"),
    )

    name = models.CharField(
        max_length=50,
        choices=CHOICES,
        default="dress",
        unique=True,
    )

    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=True,
    )

    profile_image = models.ImageField(
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
