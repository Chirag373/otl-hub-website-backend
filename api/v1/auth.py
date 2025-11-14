from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from api.v1.serializer import SignupSerializer
from api.v1.serializer import LoginSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from core.models import User


class SignupView(APIView):
    """
    View for user signup - supports both GET (list users) and POST (create user)
    """

    permission_classes = (AllowAny,)

    def get(self, request):
        """
        Get all signup data (users)
        """
        users = User.objects.all().order_by("-created_at")
        serializer = SignupSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create new user signup
        """
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "message": "User created successfully",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "phone_number": user.phone_number,
                    "role": user.role,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """
    View for user login
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response(
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "phone_number": user.phone_number,
                    "role": user.role,
                },
            },
            status=status.HTTP_200_OK,
        )
