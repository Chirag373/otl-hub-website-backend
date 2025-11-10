from django.urls import path
from api.v1.auth import SignupView

urlpatterns = [
    path('auth/signup/', SignupView.as_view(), name='signup'),
]