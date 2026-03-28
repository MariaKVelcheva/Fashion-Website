from django.db import models


class Size(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        default="",
    )

    def __str__(self):
        return self.name

