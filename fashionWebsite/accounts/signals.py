from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from fashionWebsite.accounts.models import Customer


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(
            user=instance,
            first_name="",
            last_name="",
            address="",
            telephone_number="",
        )
