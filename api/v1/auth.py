from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle
from api.v1.serializer import SignupSerializer, LoginSerializer, UserResponseSerializer, VerifyOTPSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login
from core.models import User, PendingSignup
from core.mail import send_verification_email, generate_otp
from django.db import transaction
from django.utils import timezone
from decimal import Decimal


def convert_decimals(data):
    if isinstance(data, dict):
        return {k: convert_decimals(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_decimals(v) for v in data]
    elif isinstance(data, Decimal):
        return str(data)
    return data


class SignupView(APIView):
    """
    View for user signup - POST (initiate signup with OTP)
    """

    permission_classes = (AllowAny,)
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'signup'

    def post(self, request):
        """
        Initiate signup, validate data, and send OTP
        """
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']

        # Store data temporarily
        otp = generate_otp()
        signup_data = convert_decimals(serializer.validated_data)
        
        PendingSignup.objects.update_or_create(
            email=email,
            defaults={
                'otp': otp,
                'otp_created_at': timezone.now(),
                'signup_data': signup_data
            }
        )
        
        # Send OTP
        send_verification_email(email, otp)
        
        return Response(
            {
                "message": "Please verify your email with the OTP sent.",
            },
            status=status.HTTP_200_OK,
        )


class VerifyOTPView(generics.GenericAPIView):
    """
    View for verifying OTP and completing signup
    """
    permission_classes = (AllowAny,)
    serializer_class = VerifyOTPSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'signup'

    def post(self, request):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            pending_signup = serializer.validated_data['pending_signup']
            signup_data = pending_signup.signup_data

            # Create the actual user
            signup_serializer = SignupSerializer(data=signup_data)
            if signup_serializer.is_valid(raise_exception=True):
                user = signup_serializer.save()
                
                user.is_active = True
                user.save()
                
                # Cleanup
                pending_signup.delete()

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response(
            {
                "message": "Email verified and account created successfully",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "user": UserResponseSerializer(user).data
            },
            status=status.HTTP_201_CREATED
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
