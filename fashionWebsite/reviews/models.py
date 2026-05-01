from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Review(models.Model):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

    STATUS_CHOICES = (
        (PENDING, _("Pending")),
        (APPROVED, _("Approved")),
        (REJECTED, _("Rejected")),
    )

    garment = models.ForeignKey(
        to="clothes.Garment",
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("Garment"),
    )

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("User"),
    )

    rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        verbose_name=_("Rating"),
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name=_("Status"),
    )

    text = models.TextField(
        verbose_name=_("Review Text"),
        blank=True
    )

    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now_add=True
    )

    verified_purchase = models.BooleanField(
        verbose_name=_("Verified purchase"),
        default=False
    )

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")
        unique_together = ("garment", "user")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} — {self.garment.name} ({self.rating}★)"
