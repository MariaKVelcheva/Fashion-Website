from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string


def send_custom_email(subject, message, recipient_list, html_message=None, reply_to=None):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=False,
        html_message=html_message,
        reply_to=reply_to,
    )


def send_html_email(subject: str, template_name: str, context: dict, recipient_list: list):
    html_content = render_to_string(template_name, context)
    text_content = render_to_string(template_name, context).replace('<br>', '\n')

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipient_list,
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)

