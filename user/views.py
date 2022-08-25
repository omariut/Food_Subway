from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView, ListCreateAPIView, CreateAPIView, ListAPIView
from rest_framework.views import APIView 
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from user.serializers import ChangePasswordSerializer,UserSerializer,DashBoardSerializer
from user.utils import delete_cache

User = get_user_model()


class DashBoard(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DashBoardSerializer
    queryset = User.objects.all()
    http_method_names = ['get']

    def get_queryset(self):
        return User.objects.filter(id = self.request.user.id)
    

class UserProfileCreateAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ['post']



class UserProfileRetrieveUpdateView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ['get', 'patch']





@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_password_change(request: Request) -> Response:
    user = request.user
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        if not user.check_password(serializer.data.get("old_password")):
            return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.data.get("new_password"))
        user.save()
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Password updated successfully',
            'data': []
        }
        # delete_cache(f'{request.user.username}_token_data')
        return Response(response)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def logout(request: Request) -> Response:
    if not request.user:
        raise ValidationError(detail='user not found', code=status.HTTP_404_NOT_FOUND)
    delete_cache(f'{request.user.username}_token_data')
    return Response(data={'message': 'user has been logged out'}, status=status.HTTP_200_OK)