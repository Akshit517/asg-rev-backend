from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

from users.models.user import User
from users.utils import utils
from users.serializers.user import UserSerializer
from users.mixins import PublicApiMixin

class LoginView(PublicApiMixin, APIView):
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
            access_token, refresh_token = utils.generate_tokens_for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'access_token': str(access_token),
                'refresh_token': str(refresh_token)
            })
        else:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

class RegisterView(PublicApiMixin, CreateAPIView):
    model = User
    serializer_class = UserSerializer

