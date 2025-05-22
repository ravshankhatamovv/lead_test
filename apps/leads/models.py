from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.core.validators import RegexValidator

from apps.base.models import BaseMixinModel

# Create your models here.
class Lead(BaseMixinModel):
    class LeadStatus(models.TextChoices):
        PENDING = 'pending', 'pending'
        REACHED_OUT = 'reaching_out', 'reaching_out'
    
    first_name=models.CharField(max_length=255,)
    last_name=models.CharField(max_length=255, )
    email = models.EmailField(unique=True)
    resume=models.FileField(upload_to="resumes/",)
    status=models.CharField(max_length=255, choices=LeadStatus, default=LeadStatus.PENDING.value)
    company=models.ForeignKey("company.Company", on_delete=models.SET_NULL, null=True, blank=True, db_index=True)

    def save(self, *args, **kwargs):
        self.updated_at = now()
        super(Lead, self).save(*args, **kwargs)
        return self
    
    def __str__(self):
        return f"{self.first_name}  {self.last_name}"

