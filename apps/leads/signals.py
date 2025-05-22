from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Lead
from .tasks import send_email_to_users_task

@receiver(post_save, sender=Lead)
def trigger_email_task(sender, instance, created, **kwargs):
    if created:
        send_email_to_users_task.delay(instance.id, instance.first_name, instance.last_name)
