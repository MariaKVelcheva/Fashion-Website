from django.db import models
from django.utils.translation import gettext_lazy as _


class Color(models.Model):
    name = models.CharField(
        _('name'),
        max_length=50,
        unique=True,
        default="",
    )

    hex_code = models.CharField(
        _('hex code'),
        max_length=7,
        blank=True,
        unique=True,
    )

    class Meta:
        verbose_name = _('color')
        verbose_name_plural = _('colors')

    def __str__(self):
        return self.name
