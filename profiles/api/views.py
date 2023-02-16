from rest_framework import generics, viewsets, mixins
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
# from rest_framework.viewsets import ReadOnlyModelViewSet
from profiles.models import Profile, ProfileStatus
from profiles.api.permissions import IsOwnProfileOrReadOnly, IsOwnerOrReadOnly
from profiles.api.serializers import (
    ProfileSerializer, 
    ProfileStatusSerializer, 
    ProfileAvatarSerializer,
)

class ProfileViewSet(mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """ 
        GET == list of all users profiles
        GET pk=(user id) == user publec details whiht id=pk
        
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnProfileOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["user__username"]
    
    def get_queryset(self):
        city = self.request.query_params.get("city", None)
        return (
            Profile.objects.filter(city=city)
            if city is not None
            else Profile.objects.all()
        )


class ProfileStatusViewSet(ModelViewSet):
    serializer_class = ProfileStatusSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        queryset = ProfileStatus.objects.all()
        username = self.request.query_params.get("username", None)
        if username is not None:
            queryset = queryset.filter(user_profile__user__username=username)
        return queryset
        
    def perform_create(self, serializer):
        user_profile = self.request.user.profile
        serializer.save(user_profile=user_profile)

class AvatarUpdeateView(generics.UpdateAPIView):
    serializer_class = ProfileAvatarSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        profile_object = self.request.user.profile
        return profile_object

