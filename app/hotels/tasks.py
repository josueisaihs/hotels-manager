from django.core.mail import send_mail
from django.conf import settings

from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def send_notification_email(subject, message, recipients):
    """
    Sends an email to the recipients with the subject and message

    subject: email subject
    message: email message
    recipients: list of recipient emails
    """

    send_mail(subject, message, settings.EMAIL_NO_REPLY, recipients, fail_silently=True)

    return f"Email sent to {', '.join(recipients)} successfully."
