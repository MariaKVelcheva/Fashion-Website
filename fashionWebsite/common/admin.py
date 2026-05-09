from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from fashionWebsite.common.tasks import send_email_task
from fashionWebsite.common.models import NewsletterSubscriber, Newsletter


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "subscribed_at", "is_active")
    list_filter = ("is_active",)
    search_fields = ("email",)
    list_editable = ("is_active",)
    ordering = ("-subscribed_at",)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("subject", "created_at", "is_sent")
    list_filter = ("is_sent",)
    search_fields = ("subject",)
    actions = ("send_newsletter", )

    def send_newsletter(self, request, queryset):
        already_sent = queryset.filter(is_sent=True)
        queryset = queryset.filter(is_sent=False)

        if already_sent.exists():
            self.message_user(request,
                              f"{already_sent.count()} newsletters already sent and skipped",
                              level=messages.WARNING)

        for newsletter in queryset:
            for subscriber in newsletter.active_subscribers:
                customer = get_user_model().objects.filter(email=subscriber.email).first()
                if customer:
                    name = customer.customer.full_name
                else:
                    name = _("dear customer")

                unsubscribe_url = request.build_absolute_uri(
                    reverse_lazy("newsletter-unsubscribe", args=[subscriber.token])
                )

                send_email_task.delay(
                    subject=newsletter.subject,
                    template_name="emails/newsletter.html",
                    context={
                        "email": subscriber.email,
                        "token": str(subscriber.token),
                        "name": name,
                        "body": newsletter.body,
                        "unsubscribe_url": unsubscribe_url,
                    },
                    recipient_list=[subscriber.email],
                )

            newsletter.is_sent = True
            newsletter.sent_at = timezone.now()
            newsletter.save()
