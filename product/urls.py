from django.urls import path
from product.views import ProductListCreateAPIView,PriceListCreateAPIView, CategoryListCreateAPIView

urlpatterns = [
    path('category',CategoryListCreateAPIView.as_view(),name='list_create_catagories'),
    path('products',ProductListCreateAPIView.as_view(), name='list_create_products'),
    path('variants',PriceListCreateAPIView.as_view(), name='list_create_prices'),

]