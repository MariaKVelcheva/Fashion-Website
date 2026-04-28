from django.db import models
from django.conf import settings


class Review(models.Model):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

    STATUS_CHOICES = (
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
    )

    garment = models.ForeignKey(
        to="clothes.Garment",
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)],
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default="pending",
    )

    text = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    verified_purchase = models.BooleanField(default=False)

    class Meta:
        unique_together = ("garment", "user")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} — {self.garment.name} ({self.rating}★)"
