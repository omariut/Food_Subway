from product.models import Product,Category,ProductVariant
from rest_framework import serializers
from rest_framework import serializers
from base.mixins import FieldPermissionSerializerMixin


class ProductSerializer(FieldPermissionSerializerMixin,serializers.ModelSerializer):
 



    def to_representation(self, obj):
        product_variants = obj.variant
        return {"product_variants" : ProductVariantSerializer(product_variants,many=True).data}

    # def get_product_variants(self,obj):
    #     product_variants = ProductVariant.objects.filter(product=obj)
    #     return ProductVariantSerializer(product_variants,many=True).data


    class Meta:
        model = Product
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField(read_only=True,)

    def get_products(self,obj):
        products = Product.objects.filter(category=obj)
        return ProductSerializer(products,many=True).data
    
    class Meta:
        model = Category
        fields = '__all__'

class ProductVariantSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariant
        fields = '__all__'
