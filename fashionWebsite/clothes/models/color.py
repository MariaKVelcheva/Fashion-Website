from django.db import models


class Color(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        default="",
    )

    hex_code = models.CharField(
        max_length=7,
        blank=True,
        unique=True,
    )

    def __str__(self):
        return self.name
