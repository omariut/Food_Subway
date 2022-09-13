from django.db import models
from base.models import BaseModel

# Create your models here.
class OnlinePayment(BaseModel):

    STATUS_CHOICES = (
    ("success", "success"),
    ("processing","processing"),
    ("cancelled","cancelled"),
    ("failed","failed"),
    )
    order = models.ForeignKey('order.Order', on_delete=models.PROTECT)
    amount = models.FloatField() 
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    transaction_number = models.SlugField(max_length=200, blank=False, null=False, unique=True)


    def __str__(self):
        return self.order

    class Meta:
        ordering = ['-created_at']
        db_table = 'online_payments'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),

        ]

    def __str__(self):
        return self.transaction_number