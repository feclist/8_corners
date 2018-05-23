from django.contrib.auth.models import User, Group
from backend.api.models import InstagramUser, InstagramPost, InstagramTag, InstagramLocation
from rest_framework import serializers, validators
import logging
import sys
from rest_framework.exceptions import ErrorDetail, ValidationError


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class InstagramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramUser
        fields = (
        'instagram_id', 'username', 'profile_picture', 'full_name', 'bio', 'website', 'is_business', 'counts_media',
        'counts_follows', 'counts_followed_by')


class InstagramTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramTag
        fields = '__all__'
        extra_kwargs = {
            'name': {
                'validators': [],
            }
        }


class InstagramLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramLocation
        fields = '__all__'
        extra_kwargs = {
            'instagram_id': {
                'validators': [],
            }
        }


class InstagramPostSerializer(serializers.ModelSerializer):
    tags = InstagramTagSerializer(many=True)
    user = serializers.SlugRelatedField(
        slug_field='instagram_id',
        queryset=InstagramUser.objects.all()
    )
    location = InstagramLocationSerializer()

    class Meta:
        model = InstagramPost
        fields = ('instagram_id', 'created_time', 'user_has_liked', 'likes', 'type', 'link', 'user', 'tags', 'location')

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        location = validated_data.pop('location')
        post = InstagramPost.objects.create(**validated_data)

        # Add post to user posts set
        validated_data.get('user').posts.add(post)

        loc, _ = InstagramLocation.objects.get_or_create(**location)
        post.location = loc
        post.save()

        for tag in tags:
            t, _ = InstagramTag.objects.get_or_create(**tag)
            post.tags.add(t)

        return post

# class InstagramTagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InstagramTag
#         fields = ('name',)
#
#
# class InstagramLocationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InstagramLocation
#         fields = ('id', 'latitude', 'longitude', 'name')
#
#
# class InstagramImagesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InstagramImages
#         fields = '__all__'
#
#
# class InstagramPostSerializer(serializers.ModelSerializer):
#     images = serializers.PrimaryKeyRelatedField(read_only=True)
#     tags = InstagramTagSerializer(many=True)
#     user = serializers.PrimaryKeyRelatedField(read_only=True)
#     users_in_photo = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#     location = InstagramLocationSerializer()
#
#     class Meta:
#         model = InstagramPost
#         fields = ('id', 'created_time', 'user_has_liked', 'likes', 'type', 'link', 'images', 'tags', 'location', 'user',
#                   'users_in_photo')
#
#     def create(self, validated_data):
#         # images_data = validated_data.pop('images')
#         tags = validated_data.pop('tags')
#         location = validated_data.pop('location')
#         post = InstagramPost.objects.create(**validated_data)
#
#         for tag in tags:
#             InstagramTag.objects.create(post=post, **tag)
#
#         InstagramLocation.objects.create(post=post, **location)
#
#         return post
