from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Sum
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from order.serializers import OrderSerializer,OrderItemSerializer
from order.models import Order,OrderItem


User = get_user_model()



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        extra_kwargs = {'password':{'write_only':True}, 'is_active': {'read_only': True}, 'is_superuser': {'read_only': True}, 'is_staff': {'read_only': True}, 'verified': {'read_only': True}, 'store': {'read_only': True}}
        exclude = ('groups', 'user_permissions')

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class DashBoardSerializer (UserSerializer):
    active_orders = serializers.SerializerMethodField(read_only=True)
    other_orders = serializers.SerializerMethodField(read_only=True)

    def get_active_orders(self,obj):
        active_orders = Order.objects.filter(status='on_the_way')
        return OrderSerializer(active_orders,many=True).data
    
    def get_other_orders(self,obj):
        other_orders = Order.objects.filter().exclude(status='on_the_way')
        return OrderSerializer(other_orders,many=True).data



