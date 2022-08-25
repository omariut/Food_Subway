from django.urls import path
from product.views import ProductListCreateAPIView,ProductVariantListCreateAPIView, CategoryListCreateAPIView

urlpatterns = [
    path('category',CategoryListCreateAPIView.as_view(),name='list_create_catagories'),
    path('products',ProductListCreateAPIView.as_view(), name='list_create_products'),
    path('variants',ProductVariantListCreateAPIView.as_view(), name='list_create_prices'),

]