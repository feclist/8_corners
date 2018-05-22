from django.contrib.auth.models import User, Group
from rest_framework import viewsets

from rest_framework import mixins
from rest_framework import generics
from backend.api.serializers import UserSerializer, GroupSerializer, InstagramUserSerializer, InstagramPostSerializer

from backend.api.models import InstagramUser, InstagramPost
from rest_framework import status
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class InstagramUserViewSet(viewsets.ModelViewSet):
    """
    List all Instagram Users, or create a new Instagram User.
    """
    queryset = InstagramUser.objects.all()
    serializer_class = InstagramUserSerializer

    def create(self, request, *args, **kwargs):
        counts = request.data['counts']
        request.data.update({'counts_media': counts['media'], 'counts_follows': counts['follows'],
                             'counts_followed_by': counts['followed_by']})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class InstagramPostsViewSet(viewsets.ModelViewSet):
    queryset = InstagramPost.objects.all()
    serializer_class = InstagramPostSerializer
