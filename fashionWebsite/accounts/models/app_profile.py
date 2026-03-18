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

    telephone_number = models.CharField(
        max_length=20,
    )

    size = models.CharField(
        max_length=10,
        null=True,
        blank=True,
    )

    favorites = models.ManyToManyField(
        to="clothes.Garment",
    )

    @property
    def past_orders(self):
        return self.user.orders.order_by('-created_at')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'