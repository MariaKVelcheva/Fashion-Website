from django.db import models
from django.utils.translation import gettext_lazy as _


class Size(models.Model):
    name = models.CharField(
        _("name"),
        max_length=50,
        unique=True,
        default="",
    )

    class Meta:
        verbose_name = _("size")
        verbose_name_plural = _("sizes")

    def __str__(self):
        return self.name

