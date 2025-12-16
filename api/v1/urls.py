from django.urls import path
from api.v1.auth import SignupView, VerifyOTPView
from api.v1.auth import LoginView
from api.v1.views import BuyerProfileView, RealtorProfileView, SellerProfileView
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

urlpatterns = [
    path("auth/signup/", SignupView.as_view(), name="signup"),
    path("auth/verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path("buyer/profile/", BuyerProfileView.as_view(), name="buyer-profile"),
    path("realtor/profile/", RealtorProfileView.as_view(), name="realtor-profile"),
    path("seller/profile/", SellerProfileView.as_view(), name="seller-profile"),
]
