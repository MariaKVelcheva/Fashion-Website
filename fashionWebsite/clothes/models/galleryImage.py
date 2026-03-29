from django.db import models


class GarmentImage(models.Model):
    garment = models.ForeignKey(
        to="clothes.Garment",
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="garments/")
