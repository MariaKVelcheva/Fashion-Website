import os

from django.contrib import messages
from django.core.mail import send_mail
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from fashionWebsite.common.forms import ContactForm
from django.conf import settings

from fashionWebsite.common.utils.email import send_custom_email, send_html_email


class BaseView(TemplateView):
    template_name = "common/home.html"


class ContactView(FormView):
    template_name = "common/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact")

    def form_valid(self, form):
        send_custom_email(
            subject=f"New Contact Form Submission from {form.cleaned_data['name']}",
            message=form.cleaned_data['message'],
            recipient_list=["maria.k.velcheva@gmail.com"],
        )

        send_html_email(
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

