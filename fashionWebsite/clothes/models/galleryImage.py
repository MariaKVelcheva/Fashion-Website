from django.db import models
from django.utils.translation import gettext_lazy as _


class GarmentImage(models.Model):
    garment = models.ForeignKey(
        to="clothes.Garment",
        on_delete=models.CASCADE,
        verbose_name=_("Garment"),
        related_name="images",
    )
    image = models.ImageField(
        verbose_name=_("Image"),
        upload_to="garmentImages/",
    )

    class Meta:
        verbose_name = _("Garment Image")
        verbose_name_plural = _("Garment Images")
