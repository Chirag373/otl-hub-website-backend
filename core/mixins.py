from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from core.models import User

class RoleRequiredMixin(UserPassesTestMixin):
    allowed_roles = []

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in self.allowed_roles

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            # Redirect to their appropriate dashboard based on their role
            if self.request.user.role == User.UserRole.BUYER:
                return redirect('buyer_dashboard')
            elif self.request.user.role == User.UserRole.SELLER:
                return redirect('seller_dashboard')
            elif self.request.user.role == User.UserRole.REALTOR:
                return redirect('realtor_dashboard')
            elif self.request.user.role == User.UserRole.PARTNER:
                return redirect('partner_dashboard')
        return super().handle_no_permission()

class BuyerRequiredMixin(RoleRequiredMixin):
    allowed_roles = [User.UserRole.BUYER]

class SellerRequiredMixin(RoleRequiredMixin):
    allowed_roles = [User.UserRole.SELLER]

class RealtorRequiredMixin(RoleRequiredMixin):
    allowed_roles = [User.UserRole.REALTOR]

class PartnerRequiredMixin(RoleRequiredMixin):
    allowed_roles = [User.UserRole.PARTNER]
