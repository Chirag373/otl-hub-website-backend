"""
URL configuration for otlhubs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import (
    IndexView, AboutView, LoginView, SignupView,
    BuyerDashboardView, SellerDashboardView, SellerSettingsView, SellerPropertyView,
    RealtorDashboardView, RealtorSettingsView, RealtorClientsView, PartnerDashboardView, PartnerSettingsView,
    PartnersView, BuyerPropertySearchView, BuyerFavoritesView, BuyerSettingsView,
    TermsOfServiceView, PrivacyPolicyView, PropertyDetailView, PublicPropertySearchView
)

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.v1.urls")),
    
    # Core pages
    path("", IndexView.as_view(), name="index"),
    path("index", IndexView.as_view(), name="index_html"), # For frontend template compatibility
    path("about", AboutView.as_view(), name="about"),
    path("partners", PartnersView.as_view(), name="partners"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(next_page='index'), name="logout"),
    path("signup", SignupView.as_view(), name="signup"),
    path("property-search", PublicPropertySearchView.as_view(), name="public_property_search"),
    path("property/detail", PropertyDetailView.as_view(), name="property_detail"),
    path("terms-of-service", TermsOfServiceView.as_view(), name="terms_of_service"),
    path("privacy-policy", PrivacyPolicyView.as_view(), name="privacy_policy"),
    
    # Dashboards
    path("buyer/dashboard", BuyerDashboardView.as_view(), name="buyer_dashboard"),
    path("buyer/property-search", BuyerPropertySearchView.as_view(), name="buyer_property_search"),
    path("buyer/favorites", BuyerFavoritesView.as_view(), name="buyer_favorites"),
    path("buyer/settings", BuyerSettingsView.as_view(), name="buyer_settings"),
    path("seller/dashboard", SellerDashboardView.as_view(), name="seller_dashboard"),
    path("seller/property", SellerPropertyView.as_view(), name="seller_property"),
    path("seller/settings", SellerSettingsView.as_view(), name="seller_settings"),
    path("realtor/dashboard", RealtorDashboardView.as_view(), name="realtor_dashboard"),
    path("realtor/clients", RealtorClientsView.as_view(), name="realtor_clients"),
    path("realtor/settings", RealtorSettingsView.as_view(), name="realtor_settings"),
    path("partner/dashboard", PartnerDashboardView.as_view(), name="partner_dashboard"),
    path("partner/settings", PartnerSettingsView.as_view(), name="partner_settings"),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
