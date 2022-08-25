from django.db import models
from base.models import BaseModel
from django.contrib.auth import get_user_model
User= get_user_model()

# Create your models here.
class Order(BaseModel):
    STATUS_CHOICES = (
    ("pending", "pending"),
    ("confirmed", "confirmed"),
    ("on_the_way", "on_the_way"),
    ("delivered", "delivered"),
    ("cancelled","cancelled")
)
    customer = models.ForeignKey(User, on_delete=models.PROTECT)
    address = models.TextField()
    delivery_charge = models.FloatField(default=0)
    total_without_delivery_charge = models.FloatField(default=0)
    status =  models.CharField(max_length=20, choices=STATUS_CHOICES, default='on_the_way' )

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product_variant = models.ForeignKey('product.ProductVariant', on_delete=models.PROTECT)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    sub_total = models.FloatField()



