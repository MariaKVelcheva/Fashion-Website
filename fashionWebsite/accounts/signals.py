from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db.models.signals import post_save, post_migrate
from django.conf import settings
from fashionWebsite.accounts.models import Customer
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import Group
from fashionWebsite.accounts.models import Customer
from fashionWebsite.common.utils.email import send_custom_email, send_html_email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_and_assign_group(sender, instance, created, **kwargs):
    if created:
        customer_group, _ = Group.objects.get_or_create(name="Customers")
        instance.groups.add(customer_group)

        first = last = ""
        try:
            social_account = instance.socialaccount_set.first()
            if social_account:
                extra_data = social_account.extra_data
                first = extra_data.get("given_name", "")
                last = extra_data.get("family_name", "")
        except:
            pass

        Customer.objects.get_or_create(
            user=instance,
            defaults={
                "first_name": first,
                "middle_name": "",
                "last_name": last,
                "address": "",
                "telephone_number": "",
            }
        )


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    for group_name in ["Customers", "Administrators"]:
        Group.objects.get_or_create(name=group_name)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def send_welcome_email(sender, instance, created, **kwargs):
    if not instance.email:
        return

    if created:
        send_html_email(
            subject="Welcome to Fashion Website!",
            template_name="emails/welcome.html",
            context={"user": instance},
            recipient_list=[instance.email],
        )