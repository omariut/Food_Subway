"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.urls import path
from product import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from config import settings
from django.urls.conf import re_path
from django.conf.urls.static import static


schema_view = get_schema_view(
    openapi.Info(
        title="Food Subway",
        default_version='v1.0',
        description="Api description",
        contact=openapi.Contact(email="omarcpgcbl@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,
    permission_classes=(permissions.IsAuthenticated,),
)
v1_patterns = [
    path('home/', views.HomeView.as_view()),
    path('users/', include('user.urls',),),
    path('products/', include('product.urls',),),
    path('orders/', include('order.urls',),)

]
urlpatterns = [
    # path('', health_check),
    path('api/', include([
        path('v1.0/', include(v1_patterns))
    ])),
    path('admin/', admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    ]
