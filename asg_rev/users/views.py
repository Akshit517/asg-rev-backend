from users.serializers.user import UserSerializer
from django.contrib.auth import authenticate
from users.models.user import User

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)  
            username = user.username  
            user = authenticate(username=username, password=password)  
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response(
                {"error": "Invalid credentials"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

class RegisterView(CreateAPIView):
    model = User
    permission_classes = [ permissions.AllowAny ]
    serializer_class = UserSerializer
    