from django.conf import settings
from django.db import models


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # for unsubscribe later

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["-subscribed_at"]



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