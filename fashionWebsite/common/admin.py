from django.contrib import admin, messages
from django.utils import timezone

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

        if already_sent:
            self.message_user(request, f"{already_sent.count()} newsletters already sent and skipped")

        for newsletter in queryset:
            for subscriber in newsletter.active_subscribers:
                send_email_task.delay(
                    subject=newsletter.subject,
                    template_name="emails/newsletter.html",
                    context={
                        "email": subscriber.email,
                        "token": str(subscriber.token),
                    },
                    recipient_list=[subscriber.email],
                )

            newsletter.is_sent = True
            newsletter.sent_at = timezone.now()
            newsletter.save()
