import requests
from urllib.parse import urlencode
from django.conf import settings
from django.shortcuts import redirect
from django.core.exceptions import ValidationError

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'

def verify_state_param(state: str) -> bool:
    pass
def generate_tokens_for_user(user):
    serializer = TokenObtainPairSerializer()
    token_data = serializer.get_token(user)
    access_token = token_data.access_token
    refresh_token = token_data
    return access_token, refresh_token

def get_access_token(*, code: str, redirect_uri: str, o_provider: str) -> str:
    if o_provider == "channeli":
        client_id = settings.CHANNELI_OAUTH2['CLIENT_ID']
        client_secret = settings.CHANNELI_OAUTH2['CLIENT_SECRET']
        token_url = settings.CHANNELI_OAUTH2['BASE_URL'] + '/open_auth/token/'
        print(token_url)
    elif o_provider == "google":
        client_id = settings.GOOGLE_OAUTH2['CLIENT_ID']
        client_secret = settings.GOOGLE_OAUTH2['CLIENT_SECRET']
        token_url = GOOGLE_ACCESS_TOKEN_OBTAIN_URL
    else:
        raise ValueError("Unsupported OAuth provider")

    data = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }

    response = requests.post(token_url, data=data)

    if not response.ok:
        raise ValidationError(f'Failed to obtain access token from {o_provider}.')

    access_token = response.json().get('access_token')

    return access_token

def get_user_info(*, access_token: str, o_provider: str):
    if o_provider == "channeli":
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        user_info_url = settings.CHANNELI_OAUTH2['BASE_URL'] + '/open_auth/get_user_data/' 
        response = requests.get( user_info_url, headers=headers)
    elif o_provider == "google":
        params = {
            'access_token': access_token
        }
        user_info_url = GOOGLE_USER_INFO_URL

        response = requests.get(
            GOOGLE_USER_INFO_URL,
            params= params
            )  
    else:
        raise ValueError("Unsupported OAuth provider")
    
    if not response.ok:
        raise ValidationError(f'Failed to obtain user info from {o_provider}.')

    return response.json()
