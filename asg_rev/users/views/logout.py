from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        refresh_token = self.request.data.get('refresh_token')
        if not refresh_token:
            raise ValidationError(
                {'refresh_token': ['This field is required']}
            )
        token = RefreshToken(refresh_token)
        if token:
            token.blacklist()
        return Response({"status": "refresh token blacklisted"}, status=204)

