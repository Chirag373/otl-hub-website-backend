from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Create a router for API endpoints
router = DefaultRouter()

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
]
