from rest_framework import serializers
from order.models import Order,OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ['created_at','updated_at']

class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField(read_only=True)

    def get_items(self,obj):
        items = OrderItem.objects.filter(order=obj)
        return OrderItemSerializer(items,many=True).data

    class Meta:
        model = Order
        fields ='__all__'

