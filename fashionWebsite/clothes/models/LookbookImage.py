from django.db import models

class LookbookImage(models.Model):
    image = models.ImageField(upload_to="lookbook/")
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.caption or f"Lookbook image #{self.pk}"

