from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.core.validators import RegexValidator

from apps.base.models import BaseMixinModel

# Create your models here.
class Company(BaseMixinModel):
    name=models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.updated_at = now()
        super(Company, self).save(*args, **kwargs)
        return self
    
    def __str__(self):
        return self.name