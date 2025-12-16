from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle
from api.v1.serializer import SignupSerializer, LoginSerializer, UserResponseSerializer, VerifyOTPSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login
from core.models import User
from core.mail import send_otp_email
from django.db import transaction


class SignupView(APIView):
    """
    View for user signup - POST (create user)
    """

    permission_classes = (AllowAny,)
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'signup'

    def post(self, request):
        """
        Create new user signup
        """
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Send OTP
        send_otp_email(user.email)
        
        user_data = UserResponseSerializer(user).data
        
        return Response(
            {
                "message": "User created successfully. Please verify your email.",
                "user": user_data,
            },
            status=status.HTTP_201_CREATED,
        )


class VerifyOTPView(generics.GenericAPIView):
    """
    View for verifying OTP with expiration and robust validation
    """
    permission_classes = (AllowAny,)
    serializer_class = VerifyOTPSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'signup'

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get the validated user from the serializer
        user = serializer.validated_data['user']

        # Atomic transaction ensures data integrity
        with transaction.atomic():
            user.is_active = True
            user.otp = None 
            user.otp_created_at = None # Clean up timestamp
            user.save()

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response(
            {
                "message": "Email verified successfully",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "user": UserResponseSerializer(user).data
            },
            status=status.HTTP_200_OK
        )


class LoginView(APIView):
    """
    View for user login
    """

    permission_classes = (AllowAny,)
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'login'

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        # Update last login time
        update_last_login(None, user)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        user_data = UserResponseSerializer(user).data

        return Response(
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user_data,
            },
            status=status.HTTP_200_OK,
        )
