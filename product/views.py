from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from product.serializers import ProductSerializer,ProductVariantSerializer, CategorySerializer
from product.models import Category, Product,ProductVariant
from django.db.models import Count,Sum
from rest_framework.response import Response
from rest_framework import status

from rest_framework.pagination import LimitOffsetPagination
# Create your views here.



class HomeView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer

    def list(self, request):
        new = Product.objects.all().order_by('-created_at')[:10]
        popular = Product.objects.annotate(total_order = Sum('variant__orderitem__quantity')).filter().order_by('-total_order')[:10]
        return Response({"popular": ProductSerializer(popular,many=True).data,
                        "new": ProductSerializer(new,many=True).data,},
                        status=status.HTTP_200_OK)

class CategoryListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    queryset = Category.objects.filter()


class ProductListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer
    queryset = Product.objects.filter()

class ProductVariantListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductVariantSerializer
    queryset = ProductVariant.objects.filter()

