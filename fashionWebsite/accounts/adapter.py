from allauth.core.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import redirect

from fashionWebsite.accounts.models import Customer

AppUser = get_user_model()


class AppUserSocialAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            return

        email_address = sociallogin.account.extra_data.get("email")
        if email_address:
            try:
                user = AppUser.objects.get(email=email_address)
                sociallogin.connect(request, user)
                raise ImmediateHttpResponse(redirect(settings.LOGIN_REDIRECT_URL))
            except AppUser.DoesNotExist:
                pass

    def is_auto_signup_allowed(self, request, sociallogin):
        email_address = sociallogin.account.extra_data.get("email")
        return email_address is not None

    def save_user(self, request, sociallogin, form=None):
        sociallogin.user._skip_signal = True
        user = super().save_user(request, sociallogin, form)

        extra_data = sociallogin.account.extra_data
        first = extra_data.get("given_name", "")
        last = extra_data.get("family_name", "")

        Customer.objects.get_or_create(
            user=user,
            defaults={
                "first_name": first,
                "middle_name": "",
                "last_name": last,
                "address": "",
                "telephone_number": "",
            }
        )

        customer_group, _ = Group.objects.get_or_create(name="Customers")
        user.groups.add(customer_group)

        return user