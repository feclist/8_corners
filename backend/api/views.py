from django.contrib.auth.models import User, Group
from rest_framework import viewsets

from rest_framework import mixins
from rest_framework import generics
from backend.api.serializers import UserSerializer, GroupSerializer, InstagramUserSerializer, InstagramPostSerializer
from backend.api.utils import get_object_or_none

from backend.api.models import InstagramUser, InstagramPost
from rest_framework import status
from rest_framework.response import Response

from eight_scrape.ig.profile_scrape import InstagramProfileScraper
from decouple import config


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
        scraper = InstagramProfileScraper(access_token=config('ACCESS_TOKEN'),
                                          client_secret=config('CLIENT_SECRET'),
                                          client_id=config('CLIENT_ID'))

        profile_data, posts_data = scraper.build_profile()
        profile_serializer = InstagramUserSerializer(get_object_or_none(InstagramUser, instagram_id=profile_data['id']),
                                                     data=profile_data)

        if profile_serializer.is_valid(raise_exception=True):
            profile_serializer.save()
            for post in posts_data:
                post_serializer = InstagramPostSerializer(get_object_or_none(InstagramPost, instagram_id=post['id']),
                                                          data=post)
                if post_serializer.is_valid(raise_exception=True):
                    post_serializer.save()

        headers = self.get_success_headers(profile_serializer.data)
        return Response(profile_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class InstagramPostsViewSet(viewsets.ModelViewSet):
    queryset = InstagramPost.objects.all()
    serializer_class = InstagramPostSerializer
