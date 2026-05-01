from django.contrib.auth import models as auth_models, get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from fashionWebsite.accounts.managers import AppManager


class AppUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        _("Email address"),
        unique=True,
    )

    loyalty_points = models.IntegerField(
        _("Points"),
        default=0,
    )

    is_staff = models.BooleanField(
        _("Staff status"),
        default=False
    )

    is_active = models.BooleanField(
        _("Active"),
        default=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = AppManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("App User")
        verbose_name_plural = _("App Users")

