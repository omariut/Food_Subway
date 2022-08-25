from django.contrib import admin
from product.models import Product,ProductVariant,Category
# Register your models here.
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(Category)