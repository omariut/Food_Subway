from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from user import views

urlpatterns = [
    #path('hello/', views.HelloView.as_view(), name='hello'),
    path('signup', views.UserProfileCreateAPIView.as_view(), name='profile_create'), 
    path('profile/<int:pk>', views.UserProfileRetrieveUpdateView.as_view(), name='profile_view_update'), 
    path('change_password',views.user_password_change,name='password_change'),
    path('login', jwt_views.TokenObtainPairView.as_view(), name='login'), 
    path('logout', views.logout, name='logout'),
    path('dashboard',views.DashBoard.as_view(),name='dashboard')
]
