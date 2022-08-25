from django.db import models
from base.models import BaseModel

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    

class Product(BaseModel):
    category = models.ForeignKey('product.Category',  on_delete=models.PROTECT, related_name='products',)
    name = models.CharField(max_length=100,unique=True)
    image = models.ImageField(upload_to='images', null=True, blank=True,)

    def __str__(self):
        return self.name
    

class ProductVariant(BaseModel):

    UNIT_CHOICES = (
    ("kg", "kg"),
    ("ltr", "ltr"),
    ("gm", "gm"),
    ("mL", "mL"),
)
    product = models.ForeignKey('product.Product',  on_delete=models.PROTECT, related_name='variant')
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, )
    amount = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return (self.product.name + str(self.amount)+str(self.unit))
    

