from django.urls import path
from order.views import OrderListCreateAPIView

urlpatterns = [
    path('orders',OrderListCreateAPIView.as_view(),name='list_create_orders'),
]