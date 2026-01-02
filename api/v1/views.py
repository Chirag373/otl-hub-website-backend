from rest_framework.generics import RetrieveUpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from api.v1.serializer import (
    BuyerProfileSerializer,
    RealtorProfileSerializer,
    SellerProfileSerializer,
    PropertySearchSerializer,
    PartnerProfileSerializer,
    PricingPlanSerializer,
    BuyerRealtorConnectionSerializer,
)
from core.permissions import IsBuyer, IsRealtor, IsSeller, IsPartner
from api.models import BuyerProfile, RealtorProfile, SellerProfile, PartnerProfile, PropertyImage, PricingPlan, BuyerRealtorConnection
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from api.filters import PropertyFilter, PartnerFilter



class BuyerProfileView(RetrieveUpdateAPIView):
    """
    View for Buyer profile
    """

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
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {"message": "Buyer profile updated successfully", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class RealtorProfileView(RetrieveUpdateAPIView):
    """
    View for Realtor profile
    """

    permission_classes = [IsAuthenticated, IsRealtor]
    serializer_class = RealtorProfileSerializer

    def get_object(self):
        user = self.request.user
        return RealtorProfile.objects.get(user=user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {"message": "Realtor profile updated successfully", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class SellerProfileView(RetrieveUpdateAPIView):
    """
    View for Seller profile
    """

    permission_classes = [IsAuthenticated, IsSeller]
    serializer_class = SellerProfileSerializer

    def get_object(self):
        user = self.request.user
        return SellerProfile.objects.get(user=user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {"message": "Seller profile updated successfully", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class PropertyImageDeleteView(DestroyAPIView):
    """
    View to delete a specific property image
    """
    permission_classes = [IsAuthenticated, IsSeller]
    queryset = PropertyImage.objects.all()
    
    def get_queryset(self):

        return PropertyImage.objects.filter(seller_profile__user=self.request.user)

    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class PropertySearchView(ListAPIView):
    """
    Public View (for Buyers) to search properties
    """
    permission_classes = [AllowAny]
    serializer_class = PropertySearchSerializer
    pagination_class = LimitOffsetPagination
    queryset = SellerProfile.objects.filter(has_active_listing=True).select_related('user').prefetch_related('images')
    
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    
    filterset_class = PropertyFilter
    
    ordering_fields = ['estimated_value', 'created_at']
    ordering = ['-created_at'] 

class BuyerFavoritesView(ListAPIView):
    """
    List all favorite properties for the logged-in buyer.
    """
    permission_classes = [IsAuthenticated, IsBuyer]
    serializer_class = PropertySearchSerializer
    
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PropertyFilter
    ordering_fields = ['estimated_value', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):

        buyer_profile = get_object_or_404(BuyerProfile, user=self.request.user)
        return buyer_profile.favorites.all().select_related('user').prefetch_related('images')


class BuyerFavoriteToggleView(APIView):
    """
    Toggle a property as favorite for the logged-in buyer.
    POST /api/v1/buyer/favorites/<property_id>/
    """
    permission_classes = [IsAuthenticated, IsBuyer]

    def post(self, request, property_id):
        buyer_profile = get_object_or_404(BuyerProfile, user=request.user)
        property_obj = get_object_or_404(SellerProfile, pk=property_id)
        
        if property_obj in buyer_profile.favorites.all():
            buyer_profile.favorites.remove(property_obj)
            return Response({"status": "removed", "is_favorite": False}, status=status.HTTP_200_OK)
        else:
            buyer_profile.favorites.add(property_obj)
            return Response({"status": "added", "is_favorite": True}, status=status.HTTP_201_CREATED)
            
    def get(self, request, property_id):
        """Check if a specific property is a favorite"""
        buyer_profile = get_object_or_404(BuyerProfile, user=request.user)
        is_fav = buyer_profile.favorites.filter(pk=property_id).exists()
        return Response({"is_favorite": is_fav})


class PartnerProfileView(RetrieveUpdateAPIView):
    """
    View for Partner profile
    """

    permission_classes = [IsAuthenticated, IsPartner]
    serializer_class = PartnerProfileSerializer

    def get_object(self):
        user = self.request.user
        return PartnerProfile.objects.get(user=user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {"message": "Partner profile updated successfully", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class PartnerListView(ListAPIView):
    """
    Public View to list all partners
    """
    permission_classes = [AllowAny]
    serializer_class = PartnerProfileSerializer
    queryset = PartnerProfile.objects.all().select_related('user')
    
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PartnerFilter
    ordering_fields = ['company_name', 'created_at']
    ordering = ['-created_at']


class ChangePasswordView(APIView):
    """
    View to handle user password change
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        if not current_password or not new_password:
             return Response({"error": "Both fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(current_password):
            return Response({"error": "Incorrect current password"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)


class DeleteAccountView(APIView):
    """
    View to delete user account
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "Account deleted successfully"}, status=status.HTTP_200_OK)


class UpdateNotificationSettingsView(APIView):
    """
    View to update user notification settings
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):

        return Response({"message": "Notification settings updated"}, status=status.HTTP_200_OK)


class PricingPlanListView(ListAPIView):
    """
    Public View to list all pricing plans
    """
    permission_classes = [AllowAny]
    serializer_class = PricingPlanSerializer
    queryset = PricingPlan.objects.all()


class PricingPlanUpdateView(RetrieveUpdateAPIView):
    """
    Admin View to update a pricing plan
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = PricingPlanSerializer
    queryset = PricingPlan.objects.all()
    lookup_field = 'plan_type'





from api.models import AccessPassType
from api.v1.serializer import AccessPassTypeSerializer
from rest_framework import viewsets

class AccessPassTypeViewSet(viewsets.ModelViewSet):
    """
    CRUD for Access Pass Types (Admin only for write, All for read?)
    Actually, mostly Admin. Public might need read-only.
    """
    queryset = AccessPassType.objects.all()
    serializer_class = AccessPassTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser] # Restrict to admin for now

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
             return [AllowAny()]
        return super().get_permissions()


class RealtorListView(ListAPIView):
    permission_classes = [IsAuthenticated] 
    serializer_class = RealtorProfileSerializer
    queryset = RealtorProfile.objects.all().select_related('user')
    filter_backends = [OrderingFilter] # Add SearchFilter if using standard search
    
    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.query_params.get('search', None)
        if query:
            qs = qs.filter(
                Q(user__first_name__icontains=query) | 
                Q(user__last_name__icontains=query) |
                Q(company_brokerage__icontains=query) |
                Q(location__icontains=query)
            )
        return qs

class ConnectionRequestCreateView(APIView):
    permission_classes = [IsAuthenticated, IsBuyer]
    
    def post(self, request):
        serializer = BuyerRealtorConnectionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
             try:
                 serializer.save()
                 return Response(serializer.data, status=status.HTTP_201_CREATED)
             except Exception as e:
                 return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RealtorRequestsListView(ListAPIView):
    permission_classes = [IsAuthenticated, IsRealtor]
    serializer_class = BuyerRealtorConnectionSerializer
    
    def get_queryset(self):
         return BuyerRealtorConnection.objects.filter(realtor__user=self.request.user, status='PENDING')

class ConnectionStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsRealtor]
    
    def post(self, request, pk):
        conn = get_object_or_404(BuyerRealtorConnection, pk=pk, realtor__user=request.user)
        action = request.data.get('action') 
        
        if action == 'accept':
            # Check if buyer already has an assigned agent?
            # Or just overwrite? The requirement says "if one agent accept the request, the other automatically rejected"
            
            with transaction.atomic():
                conn.status = 'ACCEPTED'
                conn.save()
                
                # Update Buyer's assigned agent
                buyer_profile = conn.buyer
                buyer_profile.assigned_agent = request.user
                buyer_profile.save()

                # Automatically reject other PENDING requests for this buyer
                BuyerRealtorConnection.objects.filter(
                    buyer=buyer_profile,
                    status='PENDING'
                ).exclude(id=conn.id).update(status='REJECTED')
             
            
        elif action == 'reject':
            conn.status = 'REJECTED'
            conn.save()
        else:
             return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"status": "success", "connection_status": conn.status})

class BuyerConnectionsListView(ListAPIView):
     permission_classes = [IsAuthenticated, IsBuyer]
     serializer_class = BuyerRealtorConnectionSerializer
     
     def get_queryset(self):
         return BuyerRealtorConnection.objects.filter(buyer__user=self.request.user).order_by('-updated_at')

