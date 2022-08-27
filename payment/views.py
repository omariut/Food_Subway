from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.db import IntegrityError
from base.utils import identifier_builder
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from order.models import Order
from payment.models import OnlinePayment
from payment.serializers import OnlinePaymentSerializer
from payment.service import sslcommerz_payment_create, sslcommerz_payment_validation

class CustomerSSLCommerzOrderPaymentView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OnlinePaymentSerializer

    def create(self, request, *args, **kwargs):

        order = get_object_or_404(Order, id=request.data['order'])
        if not order:
            return Response({'message': 'order not found'}, status=status.HTTP_404_NOT_FOUND)
        if OnlinePayment.objects.filter(order =order,status='success').exists():
            return Response({'message': 'Payment already completed'}, status=status.HTTP_400_BAD_REQUEST)

        # set other data for payment
        total_amount =  order.total_without_delivery_charge + order.delivery_charge     
        request.data['amount'] = total_amount
        transaction_number = identifier_builder(table_name='online_payments', prefix='OSL')
        request.data['transaction_number'] = transaction_number
        request.data['created_by'] = request.user.id
        # request.data['status'] = OnlinePaymentStatusOptions.INITIATED

        # set sslcommerz data
        sslcommerz_data = {
            'ipn_url': f'{settings.SSL_BASE_URL}/api/v1.0/payment/customer/order/sslcommerz/ipn',
            'value_a': order.id,
            'value_b': request.user.username,
            'num_of_item': 2,
            'product_name': 'a,b',
            'product_category': 'Deliverable',
            'product_profile': 'physical-goods',
            'total_amount': total_amount,
            'tran_id': request.data['transaction_number'],
            # 'success_url': f'{settings.FRONTEND_BASE_URL}/checkout/success/{order.id}',
            # 'fail_url': f'{settings.FRONTEND_BASE_URL}/checkout/fail/{order.id}',
            # 'cancel_url': f'{settings.FRONTEND_BASE_URL}/checkout/cancel/{order.id}',
        }

        
        # response from sslcommerz
        response = sslcommerz_payment_create(data=sslcommerz_data, customer=request.user)
        if not response:
            return Response({'message': 'Error response from SSlCommerz'}, status=status.HTTP_417_EXPECTATION_FAILED)
        res_data = {
            'payment_gateway_url': response['GatewayPageURL'],
            'logo': response['storeLogo'],
            'store_name': response['store_name'],
        }

        return super().create(request, *args, **kwargs)
            #return Response(res_data, status=status.HTTP_201_CREATED)
        # except IntegrityError as err:
        #     return Response({'message': 'Error initializing SSLCommerz payment'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomerSSLCommerzIPNView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        raise MethodNotAllowed(method=self.request.method)

    def post(self, request):
        try:
            if not request.data.get('tran_id') or not request.data.get('value_a') or not request.data.get('value_b'):
                return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
            online_payment = OnlinePayment.objects.get(transaction_number=request.data['tran_id'],created_by__username=request.data['value_b'],status=OnlinePaymentStatusOptions.INITIATED)
            online_payment.has_hit_ipn = True
            if not request.data.get('status') == 'VALID':
                online_payment.status = OnlinePaymentStatusOptions.CANCELLED
                online_payment.meta = self.request.data
                online_payment.updated_by = online_payment.created_by
                online_payment.save()
                return Response({'message': 'Payment is invalid'}, status=status.HTTP_400_BAD_REQUEST)
            params = {
                'val_id': request.data.get('val_id'),
            }
            response = sslcommerz_payment_validation(query_params=params)
            if not response:
                return Response({'message': 'No response from SSLCommerz validation API'}, status=status.HTTP_400_BAD_REQUEST)
            # sslcommerz_order_payment_task.delay(payment_reference=payment.payment_reference, meta_data=response)
            online_payment.status = OnlinePaymentStatusOptions.COMPLETED
            online_payment.meta = self.request.data
            online_payment.updated_by = online_payment.created_by
            online_payment.save()
            OrderPayment.objects.filter(order_id=request.data.get('value_a')).update(online_payment=online_payment)
            Order.objects.filter(id=request.data.get('value_a')).update(payment_status=PaymentStatusOptions.PAID, status=OrderStatusOptions.ORDERED)
            return Response({'message': 'Payment request received'}, status=status.HTTP_201_CREATED)
        except OnlinePayment.DoesNotExist:
            return Response({'message': 'Invalid payment attempted', 'data': request.data}, status=status.HTTP_400_BAD_REQUEST)