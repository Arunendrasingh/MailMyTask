import logging
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

from MailMyTask.custom_response import CustomResponse


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.


# Write here the Login, Logout & RegisterView.
logger = logging.getLogger("django")

# Login View


class LoginView(APIView):
    def post(self, request, format=None):
        # Implement post logic
        data = request.data
        email = data.get('email')
        password = data.get("password")
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                return CustomResponse(has_error=False, data=data)
            else:
                return CustomResponse(has_error="This Account is not active!!", status=status.HTTP_404_NOT_FOUND)

        else:
            return CustomResponse(has_error=True, errors="Invalid username & password.", status=status.HTTP_404_NOT_FOUND)
