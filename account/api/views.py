from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from rest_framework import generics, response
from .permissions import AnonPermissionOnly
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationAPIView(generics.CreateAPIView):
    permission_classes = [AnonPermissionOnly]
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()

class UserLoginAPIView(generics.GenericAPIView):

    permission_classes = [AnonPermissionOnly]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        access_token = RefreshToken.for_user(user).access_token
        refresh_token = RefreshToken.for_user(user)
        return response.Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "tokens":{"access": str(access_token),
                    "refresh": str(refresh_token)}
        })