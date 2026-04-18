import os

from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from fashionWebsite.common.forms import ContactForm, NewsletterForm
from django.conf import settings

from fashionWebsite.common.tasks import send_email_task
from fashionWebsite.common.utils.email import send_custom_email, send_html_email


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
            subject="Thank you for contacting us",
            template_name="emails/contact_reply.html",
            context={
                "user_name": form.cleaned_data['name'],
                "message": form.cleaned_data['message']
            },
            recipient_list=[form.cleaned_data['email']],
        )

        messages.success(self.request, "Your message has been successfully sent.")
        return super().form_valid(form)


class FAQView(TemplateView):
    template_name = "common/faq.html"


class SalesConditionsView(TemplateView):
    template_name = "common/sales-conditions.html"


class NewsletterSubscribeView(FormView):
    form_class = NewsletterForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        subscriber = form.save()
        send_email_task.delay(
            subject="Welcome to EllaPrimE — you're in!",
            template_name="emails/newsletter_welcome.html",
            context={
                "email": subscriber.email,
            },
            recipient_list=[subscriber.email],
        )

        messages.success(
            self.request,
            "You're subscribed! Check your inbox for a welcome email."
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.info(
            self.request,
            form.errors.get("email", ["Something went wrong."])[0]
        )
        return redirect("home")

    def get(self, request, *args, **kwargs):
        return redirect("home")