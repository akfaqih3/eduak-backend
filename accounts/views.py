from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from .serializers import (
    UserInputSerializer,
    UserOutputSerializer,
    OTPSendSerializer,
    OTPVerifySerializer,
    UserUpdateSerializer,
    UserChangePasswordSerializer
)

from .services import (
    user_create,
    send_otp,
    verify_otp,
    user_update,
    user_change_password,
    google_login
)

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from django.utils import timezone


User = get_user_model()


@extend_schema(tags=['Accounts'])
class UserCreateAPI(APIView):
    serializer_class = UserInputSerializer
    permission_classes=[]
    authentication_classes=[]
    def post(self, request):
        serializer =self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = user_create(
                serializer.data['name'],
                serializer.data['email'],
                serializer.data['role'],
                serializer.data['password'],
                serializer.data['phone'] if 'phone' in serializer.data else None 
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Accounts'])
class OTPSendAPI(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = OTPSendSerializer
    def post(self, request):
        serializer = OTPSendSerializer(data=request.data)
        if serializer.is_valid():
            if send_otp(serializer.data["email"]):
                return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Accounts'])
class OTPVerifyAPI(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = OTPVerifySerializer
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            if verify_otp(serializer.data["email"],serializer.data["otp"]):
                user = User.objects.get(email=serializer.data["email"])
                user.last_login = timezone.now()
                user.save()
                refresh = RefreshToken.for_user(user)
                
                return Response(
                    {
                        "message": "OTP verified successfully.",
                        "refresh": str(refresh),
                        "access": str(refresh.access_token)
                    },
                    status=status.HTTP_200_OK
                    )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Accounts'])
class UserProfileAPI(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = UserOutputSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@extend_schema(tags=['Accounts'])
class UserUpdateAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer
    def put(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_update(
                user,
                serializer.data['name'] if 'name' in serializer.data else None,
                serializer.data['email'] if 'email' in serializer.data else None,
                serializer.data['phone'] if 'phone' in serializer.data else None,
                serializer.data['role'] if 'role' in serializer.data else None,
                serializer.data['photo'] if 'photo' in serializer.data else None,
                serializer.data['bio'] if 'bio' in serializer.data else None,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@extend_schema(tags=['Accounts'])
class UserChangePasswordAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserChangePasswordSerializer
    def put(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_change_password(
                user,
                serializer.data['old_password'],
                serializer.data['new_password']
            )
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginByGoogleView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []
   
    def get(self, request):
        code = request.GET.get('code')
        if code is None:
            return Response({"message": "Invalid code."}, status=status.HTTP_400_BAD_REQUEST)
        refresh = google_login(code)
        if refresh:
            return Response(
                {
                    "message": "Login successfully.",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                },
                status=status.HTTP_200_OK
            )
        return Response({"message": "Invalid login."}, status=status.HTTP_400_BAD_REQUEST)

    