from django.urls import path
from api.v1.auth import SignupView
from api.v1.auth import LoginView
from api.v1.views import BuyerProfileView, RealtorProfileView, SellerProfileView
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

urlpatterns = [
    # Auth
    path("auth/signup/", SignupView.as_view(), name="signup"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
    # Buyer
    path("buyer/profile/", BuyerProfileView.as_view(), name="buyer-profile"),
    # Realtor
    path("realtor/profile/", RealtorProfileView.as_view(), name="realtor-profile"),
    # Seller
    path("seller/profile/", SellerProfileView.as_view(), name="seller-profile"),
]
