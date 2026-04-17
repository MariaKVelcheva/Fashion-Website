import os

from django.contrib import messages
from django.core.mail import send_mail
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from fashionWebsite.common.forms import ContactForm
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

