from rest_framework.generics import RetrieveUpdateAPIView, DestroyAPIView, ListAPIView
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.v1.serializer import (
    BuyerProfileSerializer,
    RealtorProfileSerializer,
    SellerProfileSerializer,
    PropertySearchSerializer,
    PartnerProfileSerializer,
)
from core.permissions import IsBuyer, IsRealtor, IsSeller, IsPartner
from api.models import BuyerProfile, RealtorProfile, SellerProfile, PartnerProfile, PropertyImage
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

# Create your views here.


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
        # Ensure user can only delete their own images
        return PropertyImage.objects.filter(seller_profile__user=self.request.user)

    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class PropertySearchView(ListAPIView):
    """
    Public View (for Buyers) to search properties
    """
    permission_classes = [AllowAny] # Or AllowAny if public
    serializer_class = PropertySearchSerializer
    
    def get_queryset(self):
        # Base queryset - optimize with select_related/prefetch_related
        # In a real app, strict filtering: has_active_listing=True
        queryset = SellerProfile.objects.filter(has_active_listing=True).select_related('user').prefetch_related('images')
        
        # If DB is empty/dev mode, might want to relax this:
        # queryset = SellerProfile.objects.all().select_related('user').prefetch_related('images')

        # Extract query params
        keywords = self.request.query_params.get('keywords')
        location = self.request.query_params.get('location')
        p_type = self.request.query_params.get('type')
        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')
        beds = self.request.query_params.get('beds')
        baths = self.request.query_params.get('baths')
        sort = self.request.query_params.get('sort')

        # Filters
        if keywords:
            queryset = queryset.filter(
                Q(property_description__icontains=keywords) | 
                Q(city__icontains=keywords) |
                Q(street_address__icontains=keywords)
                # JSONField search depends on DB backend, skipping for simple compatibility
            )
            
        if location:
            queryset = queryset.filter(
                Q(city__icontains=location) |
                Q(state__icontains=location) |
                Q(zip_code__icontains=location)
            )
            
        if p_type:
            queryset = queryset.filter(property_type__iexact=p_type)
            
        if price_min:
            queryset = queryset.filter(estimated_value__gte=price_min)
            
        if price_max and price_max != 'Infinity':
            queryset = queryset.filter(estimated_value__lte=price_max)
            
        if beds:
            queryset = queryset.filter(bedrooms__gte=beds)
            
        if baths:
            queryset = queryset.filter(bathrooms__gte=baths)
            
        # Sorting
        if sort:
            if sort == 'price-asc':
                queryset = queryset.order_by('estimated_value')
            elif sort == 'price-desc':
                queryset = queryset.order_by('-estimated_value')
            elif sort == 'newest':
                queryset = queryset.order_by('-created_at')
            # 'relevant' is default, no specific sort needed (or ID)
            
        return queryset

class BuyerFavoritesView(ListAPIView):
    """
    List all favorite properties for the logged-in buyer.
    """
    permission_classes = [IsAuthenticated, IsBuyer]
    serializer_class = PropertySearchSerializer
    
    def get_queryset(self):
        # We start from the BuyerProfile to ensure safety
        buyer_profile = get_object_or_404(BuyerProfile, user=self.request.user)
        return buyer_profile.favorites.all().select_related('user').prefetch_related('images')


from rest_framework.views import APIView

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


