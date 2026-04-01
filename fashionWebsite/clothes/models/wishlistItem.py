from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    garment = models.ForeignKey(to="clothes.Garment", on_delete=models.CASCADE,
                                related_name="favorites", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'garment')

    def __str__(self):
        return f"{self.user} - {self.garment}"