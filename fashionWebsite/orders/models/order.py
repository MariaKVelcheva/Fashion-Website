from django.contrib.auth import get_user_model
from django.db import models

AppUser = get_user_model()


class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("shipped", "Shipped"),
        ("received", "Received"),
        ("cancelled", "Cancelled"),
    )

    PAYMENT_CHOICES = (
        ("pod", "Payment on delivery"),
        ("card", "Card payment"),
        ("paypal", "PayPal"),
    )

    customer = models.ForeignKey(
        to=AppUser,
        on_delete=models.CASCADE,
        related_name='orders',
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    promotion = models.ForeignKey(
        to="orders.Promotion",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    payment_type = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default="pod",
    )

    shipping_address = models.TextField(
        blank=True,
        null=True,
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        return f"{self.payment_type} - {self.status}"