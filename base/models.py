from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseModel(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = 'active', ('active')
        INACTIVE = 'inactive', ('inactive')
        ARCHIVED = 'archived', ('archived')

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True