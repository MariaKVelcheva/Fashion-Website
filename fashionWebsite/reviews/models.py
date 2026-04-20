from django.db import models
from django.conf import settings


class Review(models.Model):
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
        choices=[(i, i) for i in range(1, 6)],  # 1-5 stars
    )

    body = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    verified_purchase = models.BooleanField(default=False)

    class Meta:
        unique_together = ("garment", "user")  # one review per garment per user
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} — {self.garment.name} ({self.rating}★)"