from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.renderers import BrowsableAPIRenderer

from accounts.models import CustomUser
from MailMyTask.custom_renderer import CustomRenderer
from accounts.serializers import RegisterUserSerializer


# Create views for registering the user

class RegisterUser(CreateAPIView):
    """This view use to create & update the user profile detail."""
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    queryset = CustomUser.objects.all()