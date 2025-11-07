# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from api.v1.serializers.buyer import BuyerSignupSerializer
from core.models import BaseUserDetails, Role
from rest_framework.permissions import AllowAny

class BuyerSignupView(viewsets.ModelViewSet):
    '''
    Buyer Signup View
    '''
    queryset = BaseUserDetails.objects.all()
    serializer_class = BuyerSignupSerializer
    permission_classes = [AllowAny]
    



