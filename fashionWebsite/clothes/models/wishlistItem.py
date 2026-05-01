from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db import models

CustomUser = get_user_model()


class WishlistItem(models.Model):
    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
        related_name="wishlist_items"
    )

    garment = models.ForeignKey(
        to="clothes.Garment",
        on_delete=models.CASCADE,
        related_name="wished",
        verbose_name=_('Garment'),
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        verbose_name=_('Created at'),
        auto_now_add=True,
        editable=True
    )

    class Meta:
        unique_together = ('user', 'garment')
        verbose_name = _('Favorite')
        verbose_name_plural = _('Favorites')

    def __str__(self):
        return f"{self.user} - {self.garment}"