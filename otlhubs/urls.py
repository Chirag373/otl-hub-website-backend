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
from core.views import (
    IndexView, AboutView, LoginView, SignupView,
    BuyerDashboardView, SellerDashboardView,
    RealtorDashboardView, PartnerDashboardView,
    PartnersView
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.v1.urls")),
    
    # Core pages
    path("", IndexView.as_view(), name="index"),
    path("index.html", IndexView.as_view(), name="index_html"), # For frontend template compatibility
    path("about.html", AboutView.as_view(), name="about"),
    path("partners.html", PartnersView.as_view(), name="partners"),
    path("login.html", LoginView.as_view(), name="login"),
    path("signup.html", SignupView.as_view(), name="signup"),
    
    # Dashboards
    path("buyer-dashboard.html", BuyerDashboardView.as_view(), name="buyer_dashboard"),
    path("seller-dashboard.html", SellerDashboardView.as_view(), name="seller_dashboard"),
    path("realtor-dashboard.html", RealtorDashboardView.as_view(), name="realtor_dashboard"),
    path("partner-dashboard.html", PartnerDashboardView.as_view(), name="partner_dashboard"),
]
