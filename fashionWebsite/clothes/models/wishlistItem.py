from django.contrib.auth import get_user_model
from django.db import models

CustomUser = get_user_model()


class WishlistItem(models.Model):
    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name="wishlist_items"
    )

    garment = models.ForeignKey(
        to="clothes.Garment",
        on_delete=models.CASCADE,
        related_name="wished",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=True
    )

    class Meta:
        unique_together = ('user', 'garment')

    def __str__(self):
        return f"{self.user} - {self.garment}"