from django.urls import path
from api.v1.auth import SignupView, VerifyOTPView
from api.v1.auth import LoginView
from api.v1.views import (
    BuyerProfileView, RealtorProfileView, SellerProfileView, PartnerProfileView, PartnerListView, 
    PropertyImageDeleteView, PropertySearchView, BuyerFavoritesView, BuyerFavoriteToggleView,
    ChangePasswordView, DeleteAccountView, UpdateNotificationSettingsView
)
from api.v1.payment import PaymentSuccessView, BillingPortalView

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
    path("partner/profile/", PartnerProfileView.as_view(), name="partner-profile"),
    path("seller/property-image/<int:pk>/", PropertyImageDeleteView.as_view(), name="delete-property-image"),
    path("buyer/property-search/", PropertySearchView.as_view(), name="property-search"),
    path("buyer/favorites/", BuyerFavoritesView.as_view(), name="buyer-favorites"),
    path("buyer/favorites/<int:property_id>/", BuyerFavoriteToggleView.as_view(), name="buyer-favorite-toggle"),

    path("partners/", PartnerListView.as_view(), name="partner-list"),
    path("user/change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("user/delete-account/", DeleteAccountView.as_view(), name="delete-account"),
    path("user/settings/", UpdateNotificationSettingsView.as_view(), name="update-settings"),
    path("payment/success/", PaymentSuccessView.as_view(), name="payment-success"),
    path("billing/portal/", BillingPortalView.as_view(), name="billing-portal"),
]
