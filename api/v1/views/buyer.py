# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from api.v1.serializers.buyer import BuyerSignupSerializer, BuyerListSerializer
from core.models import BaseUserDetails, Role
from rest_framework.permissions import AllowAny

class BuyerSignupView(viewsets.ModelViewSet):
    '''
    Buyer Signup View
    '''
    queryset = BaseUserDetails.objects.filter(role=Role.BUYER)
    permission_classes = [AllowAny]
    http_method_names = ['post', 'get']

    def get_serializer_class(self):
        if self.action == 'create':
            return BuyerSignupSerializer
        return BuyerListSerializer


    



