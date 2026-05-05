from celery import shared_task
from fashionWebsite.common.utils.email import send_html_email
from django.contrib.auth import get_user_model

from fashionWebsite.orders.models import Order

AppUser = get_user_model()


@shared_task
def send_email_task(subject, template_name, context, recipient_list):
    if "user_id" in context:
        context["user"] = AppUser.objects.filter(id=context["user_id"]).first()
        if not context["user"]:
            return

    if "order_id" in context:
        context["order"] = Order.objects.filter(id=context["order_id"]).first()

        if not context["order"]:
            return

    send_html_email(
        subject=subject,
        template_name=template_name,
        context=context,
        recipient_list=recipient_list,
    )

