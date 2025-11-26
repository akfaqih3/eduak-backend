from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)

from .views import (
    UserCreateAPI,
    UserProfileAPI,
    OTPSendAPI,
    OTPVerifyAPI,
    UserUpdateAPI,
    UserChangePasswordAPI,
    LoginByGoogleView,
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('password-reset/', include('django_rest_passwordreset.urls'), name='password_reset'),

    path('register/', UserCreateAPI.as_view(), name='user-register'),
    path('profile/', UserProfileAPI.as_view(), name='user-profile'),
    path('update/', UserUpdateAPI.as_view(), name='user-update'),
    path('change-password/', UserChangePasswordAPI.as_view(), name='user-change-password'),
    path('otp-send/', OTPSendAPI.as_view(), name='otp-send'),
    path('otp-verify/', OTPVerifyAPI.as_view(), name='otp-verify'),

    path('google/login/', LoginByGoogleView.as_view(), name='google_login'),
]