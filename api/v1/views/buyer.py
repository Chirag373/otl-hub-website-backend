# views.py
from api.v1.serializers.buyer import BuyerDashboardSerializer, BuyerSignupSerializer
from core.models import BaseUserDetails, Role
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

class BuyerSignupView(ModelViewSet):
    '''
    Buyer Signup View
    '''
    queryset = BaseUserDetails.objects.all()
    serializer_class = BuyerSignupSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']

class BuyerDashboardView(ModelViewSet):
    '''
    Buyer Dashboard View
    '''
    queryset = BaseUserDetails.objects.all()
    serializer_class = BuyerDashboardSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put']
    
    def get_object(self):
        return BaseUserDetails.objects.get(uuid=self.kwargs['uuid'])





