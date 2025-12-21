# Project-wide custom permissions
from rest_framework.permissions import BasePermission
from core.models import User


class IsBuyer(BasePermission):
    """
    Allows access only to users with role == User.UserRole.BUYER.

    Intended to be used in combination with IsAuthenticated:
        permission_classes = [IsAuthenticated, IsBuyer]

    This keeps role logic centralized and easy to reuse.
    """

    message = "Only buyers can access this resource."

    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return False

        role = getattr(user, "role", None)
        return role == User.UserRole.BUYER


class IsRealtor(BasePermission):
    """
    Allows access only to users with role == User.UserRole.REALTOR.

    Intended to be used in combination with IsAuthenticated:
        permission_classes = [IsAuthenticated, IsRealtor]

    This keeps role logic centralized and easy to reuse.
    """

    message = "Only realtors can access this resource."

    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return False

        role = getattr(user, "role", None)
        return role == User.UserRole.REALTOR


class IsSeller(BasePermission):
    """
    Allows access only to users with role == User.UserRole.SELLER.

    Intended to be used in combination with IsAuthenticated:
        permission_classes = [IsAuthenticated, IsSeller]

    This keeps role logic centralized and easy to reuse.
    """

    message = "Only sellers can access this resource."

    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return False

        role = getattr(user, "role", None)
        return role == User.UserRole.SELLER


class IsPartner(BasePermission):
    """
    Allows access only to users with role == User.UserRole.PARTNER.
    """

    message = "Only partners can access this resource."

    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return False

        role = getattr(user, "role", None)
        return role == User.UserRole.PARTNER

