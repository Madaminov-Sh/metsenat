from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView

from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth import authenticate

from users.serializers import UserSerializer, LoginSerializer
from users.models import User


class SignUpAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    

class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = request.data['username']
            password = request.data['password']
        else:
            raise ValidationError(serializer.errors)
        
        user = authenticate(request, username=username, password=password)
        
        if not user:
            raise ValidationError('bunday user mavjud emas')

        return Response(
            {
                'success': True,
                'status': status.HTTP_200_OK,
                'data': {
                    'username': user.username,
                    'email': user.email,
                    'refresh': serializer.validated_data.get('refresh'),
                    'access': serializer.validated_data.get('access'),                    
                },
            }
        )
    