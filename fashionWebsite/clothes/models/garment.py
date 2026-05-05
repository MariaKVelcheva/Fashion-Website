from datetime import timedelta
from decimal import Decimal

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class Garment(models.Model):
    category = models.ManyToManyField(
        to="clothes.Category",
        related_name='garments',
        verbose_name=_("Category"),
    )

    name = models.CharField(
        _("Garment name"),
        max_length=100,
        null=True,
        blank=True,
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    description = models.TextField(
        _("Garment description"),
        blank=True,
        null=True,
    )

    main_image = models.ImageField(
        _("Main image"),
        upload_to='garments/',
        blank=True,
        null=True,
    )

    price = models.DecimalField(
        _("Price"),
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
        null=True,
        blank=True,
        editable=True,
    )

    @property
    def is_new(self):
        return timezone.now() - self.created_at < timedelta(days=60)

    @property
    def is_available(self):
        return self.products.filter(stock__gt=0).exists()

    @property
    def rating_summary(self):
        from django.db.models import Avg, Count
        data = self.reviews.filter(status="approved").aggregate(
            avg=Avg("rating"), count=Count("id")
        )
        if data["count"] and data["count"] >= 3:
            return data
        return None

    @property
    def discounted_price(self):
        from fashionWebsite.promotions.models import Promotion

        now = timezone.now()

        garment_promotion = Promotion.objects.filter(
            garments=self,
            valid_from__lte=now,
            valid_until__gte=now,
            type="garment",
        ).first()

        category_promotion = Promotion.objects.filter(
            categories__in=self.category.all(),
            valid_from__lte=now,
            valid_until__gte=now,
            type="category",
        ).first()

        if garment_promotion and not garment_promotion.is_exhausted:
            return round((1 - garment_promotion.discount_percent / Decimal('100')) * self.price, 2)

        if category_promotion and not category_promotion.is_exhausted:
            return round((1 - category_promotion.discount_percent / Decimal('100')) * self.price, 2)

        return None

    def get_available_colors(self):
        return list({p.color for p in self.products.select_related("color")})

    def get_available_sizes(self):
        return list({p.size for p in self.products.select_related("size")})

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Garment")
        verbose_name_plural = _("Garments")

    def __str__(self):
        return self.name

