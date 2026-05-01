from django.db import models
from django.utils.translation import gettext_lazy as _


class LookbookImage(models.Model):
    image = models.ImageField(
        verbose_name=_('Image'),
        upload_to="lookbook/"
    )

    caption = models.CharField(
        verbose_name=_('Caption'),
        max_length=200,
        blank=True
    )

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

    def __str__(self):
        return self.caption or f"Lookbook image #{self.pk}"

