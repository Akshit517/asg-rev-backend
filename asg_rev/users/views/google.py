from urllib.parse import urlencode
from django.conf import settings
from django.shortcuts import redirect

from rest_framework import status
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from users.utils import utils
from users.mixins import PublicApiMixin
from users.models.user import User
from users.serializers.user import UserSerializer

class GoogleLoginApi(PublicApiMixin, APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)

    def get(self, request):
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get('code')
        error = validated_data.get('error')

        login_url = f'{settings.BASE_FRONTEND_URL}'
    
        if error or not code:
            params = urlencode({'error': error})
            return redirect(f'{login_url}?{params}')

        redirect_uri = f'{settings.BASE_FRONTEND_URL}/callback/google/'
        access_token = utils.get_access_token(
            code=code, 
            redirect_uri=redirect_uri,
            o_provider='google'
            )

        user_data = utils.get_user_info(
            access_token=access_token,
            o_provider='google'
            )

        try:
            user = User.objects.get(email=user_data.get('email'))
            access_token, refresh_token = utils.generate_tokens_for_user(user)
            response_data = {
                'user': UserSerializer(user).data,
                'access_token': str(access_token),
                'refresh_token': str(refresh_token)
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            username = user_data['name']
            user = User.objects.create(
                username=username,
                email=user_data['email'],
                profile_pic=user_data['picture'],
                auth_type='google'
            )           
            access_token, refresh_token = utils.generate_tokens_for_user(user)
            response_data = {
                'user': UserSerializer(user).data,
                'access_token': str(access_token),
                'refresh_token': str(refresh_token)
            }
            return Response(response_data, status=status.HTTP_200_OK)       