from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from users.views import (
    LoginView,
    RegisterView,
    GoogleLoginApi,
    ChanneliLoginApi,
    LogoutView,
    WrappedTokenRefreshView
)
from users.views.app_links import asset_links
from users.views.upload_media import UploadMediaView
from users.views.users import UserView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),   
    path('register/', RegisterView.as_view(), name='register'), 
    path('signin/google/', GoogleLoginApi.as_view(), name='signin-google'),
    path('signin/channeli/', ChanneliLoginApi.as_view(), name='signin-channeli'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/token/refresh/', WrappedTokenRefreshView.as_view(), name='token-refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token-verify'),
    path('.well-known/assetlinks.json', asset_links),
    path('upload-media/', UploadMediaView.as_view(), name='upload_media'),
    path('users/', UserView.as_view(), name='users'),
]