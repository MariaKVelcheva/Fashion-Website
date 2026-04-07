from celery import shared_task
from fashionWebsite.common.utils.email import send_html_email
from django.contrib.auth import get_user_model


AppUser = get_user_model()


@shared_task
def send_email_task(subject, template_name, context, recipient_list):
    if "user_id" in context:
        context["user"] = AppUser.objects.get(id=context["user_id"])

    send_html_email(
        subject=subject,
        template_name=template_name,
        context=context,
        recipient_list=recipient_list,
    )

