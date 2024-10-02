from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions as rest_exceptions

from django.core.exceptions import ValidationError

class ApiAuthMixin:
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, )

class PublicApiMixin:
    authentication_classes = ()
    permission_classes = ()

