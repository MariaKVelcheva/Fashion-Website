from django.contrib import messages
from django.core.mail import send_mail
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from fashionWebsite.common.forms import ContactForm
from django.conf import settings


class BaseView(TemplateView):
    template_name = "common/home.html"


class ContactView(FormView):
    template_name = "common/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        message = form.cleaned_data["message"]

        send_mail(
            subject=f"Message from: {name}",
            message=message,
            from_email=email,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
        )

        messages.success(self.request, "Your message has been sent successfully! 🎉")
        return super().form_valid(form)

