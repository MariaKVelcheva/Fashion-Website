from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

AppUser = get_user_model()


class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", _("Pending")),
        ("confirmed", _("Confirmed")),
        ("shipped", _("Shipped")),
        ("received", _("Received")),
        ("cancelled", _("Cancelled")),
    )

    PAYMENT_CHOICES = (
        ("pod", _("Payment on delivery")),
        ("card", _("Card payment")),
    )

    customer = models.ForeignKey(
        to=AppUser,
        on_delete=models.CASCADE,
        verbose_name=_("Customer"),
        related_name='orders',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        verbose_name=_("Status"),
        default="pending",
    )

    promotion = models.ForeignKey(
        to="promotions.Promotion",
        null=True,
        blank=True,
        verbose_name=_("Promotion"),
        on_delete=models.SET_NULL,
    )

    payment_type = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        verbose_name=_("Payment type"),
        default="pod",
    )

    shipping_address = models.TextField(
        blank=True,
        verbose_name=_("Shipping address"),
        null=True,
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("Phone number"),
        null=True,
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Total amount"),
    )

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"{self.payment_type} - {self.status}"