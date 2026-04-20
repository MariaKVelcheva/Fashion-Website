from django.conf import settings
from django.contrib.auth import get_user_model
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
            name_validator,
        ]
    )

    middle_name = models.CharField(
        max_length=100,
        validators=[
            name_validator,
        ],
        null=True,
        blank=True,
    )

    last_name = models.CharField(
        max_length=100,
        validators=[
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
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def past_orders(self):
        return self.user.orders.order_by('-created_at')

    def is_profile_complete(self):
        return (
                self.first_name and len(self.first_name.strip()) >= 3 and
                self.last_name and len(self.last_name.strip()) >= 3 and
                self.address and self.address.strip() and
                self.telephone_number and self.telephone_number.strip()
        )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

