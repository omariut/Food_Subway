from django.urls import path
from order.views import OrderListCreateAPIView, OrderRetrieveUpdateAPIView
urlpatterns = [
    path('orders',OrderListCreateAPIView.as_view(),name='list_create_orders'),
    path('order/<int:pk>',OrderRetrieveUpdateAPIView.as_view(),name='retrieve_update_order'),
]