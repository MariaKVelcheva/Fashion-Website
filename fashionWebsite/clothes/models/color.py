from django.db import models


class Color(models.Model):
    CHOICES = (
        ("red", "Red"),
        ("green", "Green"),
        ("blue", "Blue"),
        ("yellow", "Yellow"),
        ("white", "White"),
        ("black", "Black"),
        ("gray", "Gray"),
        ("brown", "Brown")
    )

    name = models.CharField(
        max_length=50,
        choices=CHOICES,
    )

    hex_code = models.CharField(
        max_length=7,
        blank=True,
    )
