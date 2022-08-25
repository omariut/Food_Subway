from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from order.models import Order,OrderItem
from product.models import ProductVariant
from order.serializers import OrderSerializer,OrderItemSerializer
from django.db import transaction
from django.shortcuts import get_object_or_404

# Create your views here.
class OrderListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer
    queryset = Order.objects.filter()
    

    def perform_create(self, serializer):
        order_items = self.request.data['items']
        order_item_objects = []
        item_total = 0

        with transaction.atomic():
            order = serializer.save()
            for item in order_items:
                
                product_variant_id = item['product_variant']
                quantity = item['quantity']
                unit_price = get_object_or_404(ProductVariant, id=product_variant_id).price
                sub_total= (quantity*unit_price)

                obj = OrderItem(order=order,
                product_variant_id=product_variant_id,
                quantity=quantity,
                unit_price=unit_price,
                sub_total=sub_total

                )
                order_item_objects.append(obj)
                item_total+=sub_total
            OrderItem.objects.bulk_create(order_item_objects)
            order.total_without_delivery_charge = item_total 
            order.save()

class OrderRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,IsAdminUser)
    serializer_class = OrderSerializer
    queryset = Order.objects.filter()

    def patch(self, request,*args,**kwargs):
        order_items = self.request.data.get('items')
        

        if order_items:

            order = self.get_object()
            order_item_objects = []
            item_total = 0

            with transaction.atomic():

                OrderItem.objects.filter(order=order).delete()
                
                for item in order_items:
                    
                    product_variant_id = item['product_variant']
                    quantity = item['quantity']
                    unit_price = get_object_or_404(ProductVariant, id=product_variant_id).price
                    sub_total= (quantity*unit_price)

                    obj = OrderItem(order=order,
                    product_variant_id=product_variant_id,
                    quantity=quantity,
                    unit_price=unit_price,
                    sub_total=sub_total

                    )
                    order_item_objects.append(obj)
                    item_total+=sub_total
                OrderItem.objects.bulk_create(order_item_objects)
                order.total_without_delivery_charge = item_total 
                order.save()
                return super().patch(request,*args,**kwargs)






