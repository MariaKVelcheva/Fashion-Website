from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from fashionWebsite.accounts.validators import name_validator

AppUser = get_user_model()


class Customer(models.Model):
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
        related_name='customer',
        primary_key=True,
    )

    first_name = models.CharField(
        _('First Name'),
        max_length=100,
        validators=[
            name_validator,
        ]
    )

    middle_name = models.CharField(
        _('Middle Name'),
        max_length=100,
        validators=[
            name_validator,
        ],
        default="",
    )

    last_name = models.CharField(
        _('Last Name'),
        max_length=100,
        validators=[
            name_validator,
        ]
    )

    address = models.TextField(
        _('Address'),
    )

    telephone_number = models.CharField(
        _('Telephone Number'),
        max_length=20,
    )

    size = models.CharField(
        _('Size'),
        max_length=10,
        null=True,
        blank=True,
    )

    favorites = models.ManyToManyField(
        to="clothes.Garment",
        verbose_name=_('Favorites'),
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

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

