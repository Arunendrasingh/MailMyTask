from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import LoginView


urlpatterns = [
    path("", LoginView.as_view(), name="auth"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
