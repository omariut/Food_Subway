from django.urls import path
from product.views import ProductListCreateAPIView,ProductVariantListCreateAPIView, CategoryListCreateAPIView,ProductUpdateAPIView

urlpatterns = [
    path('category',CategoryListCreateAPIView.as_view(),name='list_create_catagories'),
    path('products',ProductListCreateAPIView.as_view(), name='list_create_products'),
    path('products/<int:pk>',ProductUpdateAPIView.as_view(), name='updates_products'),
    path('variants',ProductVariantListCreateAPIView.as_view(), name='list_create_prices'),

]