from django.urls import include, path
from rest_framework.routers import DefaultRouter

from profiles.api.views import ProfileViewSet, ProfileStatusViewSet, AvatarUpdeateView

router = DefaultRouter()
router.register(r"profiles", ProfileViewSet, basename="profile")
router.register(r"status", ProfileStatusViewSet, basename="status")
urlpatterns = [
    path("", include(router.urls)),
    path("avatar/", AvatarUpdeateView.as_view(), name="avatar-updeate")
]
