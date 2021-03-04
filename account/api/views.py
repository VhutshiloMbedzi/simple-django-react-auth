from .serializers import UserRegistrationSerializer
from rest_framework import generics
from .permissions import AnonPermissionOnly

from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationAPIView(generics.CreateAPIView):
    permission_classes = [AnonPermissionOnly]
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()