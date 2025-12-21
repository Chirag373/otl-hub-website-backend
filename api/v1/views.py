from rest_framework.generics import RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from api.v1.serializer import (
    BuyerProfileSerializer,
    RealtorProfileSerializer,
    SellerProfileSerializer,
)
from core.permissions import IsBuyer, IsRealtor, IsSeller
from api.models import BuyerProfile, RealtorProfile, SellerProfile, PropertyImage
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
