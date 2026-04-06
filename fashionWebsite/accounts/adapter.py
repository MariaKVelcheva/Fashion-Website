from allauth.core.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

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