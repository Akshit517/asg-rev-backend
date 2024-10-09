from django.urls import path
from users.views import (
    LoginView,
    RegisterView,
    GoogleLoginApi,
    ChanneliLoginApi,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),   
    path('register/', RegisterView.as_view(), name='register'), 
    path('callback/google/', GoogleLoginApi.as_view(), name='login-google'),
    path('callback/channeli/', ChanneliLoginApi.as_view(), name='callback')
]