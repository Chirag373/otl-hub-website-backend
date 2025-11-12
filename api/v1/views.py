from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from api.v1.serializer import BuyerProfileSerializer
from core.permissions import IsBuyer
from api.models import BuyerProfile
from rest_framework.response import Response
from rest_framework import status
# Create your views here.



class BuyerProfileView(RetrieveUpdateAPIView):
    '''
    View for Buyer profile
    '''
    permission_classes = [IsAuthenticated, IsBuyer]
    serializer_class = BuyerProfileSerializer

    def get_object(self):
        user = self.request.user
        return BuyerProfile.objects.get(user=user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'message': 'Buyer profile updated successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


        

