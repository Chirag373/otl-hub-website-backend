from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from api.v1.serializer import SignupSerializer

class SignupView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer