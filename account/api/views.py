from .serializers import (  UserRegistrationSerializer, 
                            UserLoginSerializer, 
                            UserSerializer,
                            ProfileSerializer)
from rest_framework import generics, response, permissions
from .permissions import AnonPermissionOnly, IsOwnerOrReadOnly
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from account.models import Profile
from django.shortcuts import get_object_or_404, Http404

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

class ProfileAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer

    def get_object(self, *args, **kwargs):
        username = self.kwargs.get("username")
        if username is not None:
            user = get_object_or_404(User, username=username)
            obj = get_object_or_404(Profile, user=user)
            if obj == None:
                raise Http404
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_context(self, *args, **kwargs):
        user = self.request.user
        profile = self.get_object()

        is_owner = False 
        if profile.owner == user:
            is_owner = True

        return {
            'is_owner': is_owner
        }

class ProfileSearchAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    search_fields = ['user__username', 'bio', 'name']

    def get_serializer_context(self, *args, **kwargs):
        user = self.request.user
        profile = Profile.objects.get(user=user)

        is_owner = False 
        if profile.owner == user:
            is_owner = True

        return {
            'is_owner': is_owner
        }