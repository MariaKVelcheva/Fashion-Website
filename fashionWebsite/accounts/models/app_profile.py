from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

from fashionWebsite.accounts.validators import name_validator

AppUser = get_user_model()


class Customer(models.Model):
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer',
        primary_key=True,
    )

    first_name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3),
            name_validator,
        ]
    )

    last_name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3),
            name_validator,
        ]
    )

    address = models.TextField()

    telephone_number = models.CharField()

    size = models.CharField(
        max_length=10,
        null=True,
        blank=True,
    )

    favorites = models.ManyToManyField(
        to="clothes.Garment",
    )

#   past_orders = models.ManyToManyField(
#      to="clothes.Orders",)


