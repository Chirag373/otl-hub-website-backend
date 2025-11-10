from django.urls import path
from api.v1.auth import SignupView
from api.v1.auth import LoginView

urlpatterns = [
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/login/', LoginView.as_view(), name='login'),
]