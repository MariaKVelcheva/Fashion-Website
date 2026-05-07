import uuid

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

    token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name=_('Token'),
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("Newsletter Subscriber")
        ordering = ["-subscribed_at"]


class Newsletter(models.Model):
    body = models.TextField(
        verbose_name=_('Body'),
    )

    subject = models.CharField(
        max_length=255,
        verbose_name=_('Subject'),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    is_sent = models.BooleanField(
        default=False,
    )

    @property
    def active_subscribers(self):
        return NewsletterSubscriber.objects.filter(is_active=True)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = _("Newsletter")
        verbose_name_plural = _("Newsletters")
        ordering = ["-created_at"]



