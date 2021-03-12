from django.urls import path
from .views import UserRegistrationAPIView, UserLoginAPIView, ProfileAPIView, ProfileSearchAPIView

app_name = 'account'

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('profile/<str:username>/', ProfileAPIView.as_view(), name="profile"),
    path('profile-search/', ProfileSearchAPIView.as_view(), name="search_profiles")
]