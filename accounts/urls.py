from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from accounts import views


urlpatterns = [
    path('auth/', TokenObtainPairView.as_view(), name='auth'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', views.RegisterUser.as_view(), name='signup'),
]
