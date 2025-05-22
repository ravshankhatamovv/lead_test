from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser



from apps.base.models import BaseMixinModel

# Create your models here.
class CustomUser(AbstractUser, BaseMixinModel):
    class EmployeeStatus(models.TextChoices):
        PROSPECT = 'prospect', 'Prospect'
        ATTORNEY = 'attorney', 'Attorney'
        OTHER = 'other', 'Other'
    status=models.CharField(max_length=255, choices=EmployeeStatus, null=True, blank=True)
    company=models.ForeignKey("company.Company", on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.updated_at = now()

        super(CustomUser, self).save(*args, **kwargs)
        return self
    
    def __str__(self):
        return self.username
    


