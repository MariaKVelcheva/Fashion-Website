import os
import secrets
from datetime import timedelta

from django.contrib import messages
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from fashionWebsite.common.forms import ContactForm, NewsletterForm
from fashionWebsite.common.models import NewsletterSubscriber
from fashionWebsite.common.tasks import send_email_task
from fashionWebsite.common.utils.email import send_custom_email, send_html_email
from fashionWebsite.promotions.models import Promotion


class BaseView(TemplateView):
    template_name = "common/home.html"


class ContactView(FormView):
    template_name = "common/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact")

    def form_valid(self, form):
        send_custom_email(
            subject=f"EllaPrimE contact — {form.cleaned_data['name']} ({form.cleaned_data['email']})",
            message=form.cleaned_data['message'],
            html_message=f"""
                <p><strong>From:</strong> {form.cleaned_data['name']}</p>
                <p><strong>Email:</strong> {form.cleaned_data['email']}</p>
                <hr>
                <p>{form.cleaned_data['message']}</p>
            """,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            reply_to=form.cleaned_data['email'],
        )

        send_email_task.delay(
            subject=_("Thank you for contacting us"),
            template_name="emails/contact_reply.html",
            context={
                "user_name": form.cleaned_data['name'],
                "message": form.cleaned_data['message']
            },
            recipient_list=[form.cleaned_data['email']],
        )

        messages.success(self.request, _("Your message has been successfully sent."))
        return super().form_valid(form)


class FAQView(TemplateView):
    template_name = "common/faq.html"


class SalesConditionsView(TemplateView):
    template_name = "common/sales-conditions.html"


class NewsletterUnsubscribeView(TemplateView):
    template_name = "emails/newsletter-unsubscribe.html"

    def get(self, request, *args, **kwargs):
        token = kwargs["token"]
        subscriber = NewsletterSubscriber.objects.filter(token=token, is_active=True).first()

        if not subscriber:
            messages.error(request, _("Invalid request."))
            return redirect(reverse_lazy("home"))

        context = {
            "subscriber": subscriber,
        }

        return render(request, "emails/newsletter-unsubscribe.html", context)

    def post(self, request, token, *args, **kwargs):
        subscriber = NewsletterSubscriber.objects.filter(token=token, is_active=True).first()

        if not subscriber:
            messages.error(request, _("Invalid request."))
            return redirect(reverse_lazy("home"))

        subscriber.is_active = False
        subscriber.save()

        messages.success(request, _("You have successfully unsubscribed."))
        return redirect(reverse_lazy("home"))


class NewsletterSubscribeView(FormView):
    form_class = NewsletterForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        with transaction.atomic():
            subscriber = form.save()
            unsubscribe_url = self.request.build_absolute_uri(
                reverse("newsletter-unsubscribe", args=[subscriber.token])
            )
            code = f"{subscriber.email.split("@")[0].upper()}-{secrets.token_urlsafe(2).upper()}-10"

            promotion = Promotion.objects.create(
                code=code,
                type="code",
                discount_percent=10,
                valid_from=timezone.now(),
                valid_until=timezone.now() + timedelta(days=365 * 100),
                max_uses=1,
            )

        send_email_task.delay(
            subject=_("Welcome to EllaPrimE!"),
            template_name="emails/newsletter_welcome.html",
            context={
                "email": subscriber.email,
                "unsubscribe_url": unsubscribe_url,
                "promotion": promotion.code,
            },
            recipient_list=[subscriber.email],
        )

        messages.success(
            self.request,
            _("You're subscribed! Check your inbox for a welcome email.")
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.info(
            self.request,
            form.errors.get("email", [_("Something went wrong.")])[0]
        )
        return redirect("home")

    def get(self, request, *args, **kwargs):
        return redirect("home")

