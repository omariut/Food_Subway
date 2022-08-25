from product.models import Product,Category,ProductVariant
from rest_framework import serializers



class ProductSerializer(serializers.ModelSerializer):
    product_variants = serializers.SerializerMethodField(read_only=True)

    def get_product_variants(self,obj):
        product_variants = ProductVariant.objects.filter(product=obj)
        return ProductVariantSerializer(product_variants,many=True).data


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
        fields = ['unit','amount','price']
