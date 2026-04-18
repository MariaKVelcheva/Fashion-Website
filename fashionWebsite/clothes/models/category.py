from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        default="",
        unique=True,
    )

    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=True,
    )

    profile_image = models.ImageField(
        upload_to='categories/',
        null=True,
        blank=True,
    )

    trending = models.BooleanField(
        default=False,
    )

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
