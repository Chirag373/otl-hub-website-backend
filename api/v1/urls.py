from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.v1.views.buyer import BuyerSignupView

# Create a router for API endpoints
router = DefaultRouter()

router.register(r'buyer', BuyerSignupView, basename='buyer-signup')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
]
