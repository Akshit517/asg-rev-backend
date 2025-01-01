from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.response import Response
from rest_framework import status

class WrappedTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        wrapped_refresh_token = request.data.get('refresh_token')    
        if not wrapped_refresh_token:
            return Response(
                {"detail": "refresh_token field is required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        request.data['refresh'] = wrapped_refresh_token
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            data = {
                'refresh_token': wrapped_refresh_token,
                'access_token': response.data.get('access')
            }
            return Response(data, status=status.HTTP_200_OK)
        return response

