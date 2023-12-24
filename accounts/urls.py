from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView


urlpatterns = [
    path('auth/', TokenObtainPairView.as_view(), name='auth'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
