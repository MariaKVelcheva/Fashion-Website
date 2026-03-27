from django.db import models


class Size(models.Model):
    CHOICES = (
        ("xs", "XS"),
        ("s", "S"),
        ("m", "M"),
        ("l", "L"),
        ("xl", "XL"),
        ("xxl", "XXL"),
        ("uni size", "Uni size")
    )

    name = models.CharField(
        max_length=50,
        choices=CHOICES,
        unique=True,
    )

