from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from apps.account.models import CustomUser

@shared_task
def send_email_to_users_task(lead_id, first_name, last_name):
    recipients = CustomUser.objects.filter(status__in=["prospect", "attorney"]).values_list('email', flat=True)
    if recipients:
        send_mail(
            subject="Yangi Lead Yaratildi",
            message=f"Yangi lead: {first_name} {last_name} (ID: {lead_id}) yaratildi.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=list(recipients),
            fail_silently=False
        )