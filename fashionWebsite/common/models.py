from django.db import models
from django.utils.translation import gettext_lazy as _


class NewsletterSubscriber(models.Model):
    email = models.EmailField(
        unique=True,
        verbose_name=_('Email'),
    )
    subscribed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Subscribed'),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Active'),
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("Newsletter Subscriber")
        ordering = ["-subscribed_at"]
