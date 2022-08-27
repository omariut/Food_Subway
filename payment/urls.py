from django.urls import path
from payment.views import CustomerSSLCommerzOrderPaymentView, CustomerSSLCommerzIPNView


urlpatterns = [
    path('ssl-order-payment', CustomerSSLCommerzOrderPaymentView.as_view(), name='customer-ssl-order-payment'),
    path('order/sslcommerz/ipn', CustomerSSLCommerzIPNView.as_view(), name='customer-ssl-ipn'),
]