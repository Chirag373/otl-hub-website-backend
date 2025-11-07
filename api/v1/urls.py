from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.v1.views.buyer import BuyerDashboardView, BuyerSignupView

# Create a router for API endpoints
router = DefaultRouter()

router.register(r'buyer', BuyerSignupView, basename='buyer-signup')
router.register(r'buyer-dashboard/(?P<uuid>[0-9a-f-]+)/', BuyerDashboardView, basename='buyer-dashboard')
urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
]
