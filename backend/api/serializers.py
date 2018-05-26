from django.contrib.auth.models import User, Group
from backend.api.models import InstagramUser, InstagramPost, InstagramTag, InstagramLocation, InstagramImages, \
    InstagramCaption
from rest_framework import serializers

from backend.api.utils import get_nested_value, unix_to_datetime_string

from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_text
from rest_framework.utils import model_meta


class CreatableSlugRelatedField(serializers.SlugRelatedField):

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get_or_create(**{self.slug_field: data})[0]
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.slug_field, value=smart_text(data))
        except (TypeError, ValueError):
            self.fail('invalid')


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

    def to_internal_value(self, data):
        data['instagram_id'] = data['id']
        del data['id']
        data['counts_media'] = data['counts']['media']
        data['counts_follows'] = data['counts']['follows']
        data['counts_followed_by'] = data['counts']['followed_by']
        return super().to_internal_value(data)


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

    def to_internal_value(self, data):
        data['instagram_id'] = data['id']
        del data['id']
        return super().to_internal_value(data)


class InstagramImagesSerializer(serializers.ModelSerializer):
    local_map = {
        'thumbnail_width': 'thumbnail.width',
        'thumbnail_height': 'thumbnail.height',
        'thumbnail_url': 'thumbnail.url',
        'low_res_width': 'low_resolution.width',
        'low_res_height': 'low_resolution.height',
        'low_res_url': 'low_resolution.url',
        'standard_res_width': 'standard_resolution.width',
        'standard_res_height': 'standard_resolution.height',
        'standard_res_url': 'standard_resolution.url'
    }

    class Meta:
        model = InstagramImages
        fields = '__all__'

    # def to_representation(self, obj):
    #     """Move fields from profile to user representation."""
    #     representation = super().to_representation(obj)
    #     profile_representation = representation.pop('profile')
    #     for key in profile_representation:
    #         representation[key] = profile_representation[key]
    #
    #     return representation

    def to_internal_value(self, data):
        """Move fields related to profile to their own profile dictionary."""
        internal = super().to_internal_value(
            {key: get_nested_value(data, self.local_map[key]) for key in self.local_map.keys()})
        return internal

    # Might need this for future use.
    # def update(self, instance, validated_data):
    #     """Update user and profile. Assumes there is a profile for every user."""
    #     profile_data = validated_data.pop('profile')
    #     super().update(instance, validated_data)
    #
    #     profile = instance.profile
    #     for attr, value in profile_data.items():
    #         setattr(profile, attr, value)
    #     profile.save()
    #
    #     return instance


class InstagramCaptionSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='instagram_id',
        queryset=InstagramUser.objects.all()
    )

    class Meta:
        model = InstagramCaption
        fields = '__all__'
        extra_kwargs = {
            'instagram_id': {
                'validators': [],
            }
        }

    def to_internal_value(self, data):
        data['created_time'] = unix_to_datetime_string(data['created_time'])
        data['instagram_id'] = data['id']
        del data['id']
        data['user'] = data['from']['id']
        return super().to_internal_value(data=data)


class InstagramPostSerializer(serializers.ModelSerializer):
    tags = CreatableSlugRelatedField(
        many=True,
        slug_field='name',
        queryset=InstagramTag.objects.all()
    )
    user = serializers.SlugRelatedField(
        slug_field='instagram_id',
        queryset=InstagramUser.objects.all()
    )
    location = InstagramLocationSerializer()
    images = InstagramImagesSerializer()
    caption = InstagramCaptionSerializer()

    class Meta:
        model = InstagramPost
        fields = ('instagram_id', 'created_time', 'user_has_liked', 'likes', 'type', 'link', 'user', 'tags', 'location',
                  'images', 'caption', 'comments')

    def to_internal_value(self, data):
        data['instagram_id'] = data['id']
        del data['id']
        data['comments'] = data['comments']['count']
        data['likes'] = data['likes']['count']
        data['user'] = data['user']['id']
        data['created_time'] = unix_to_datetime_string(data['created_time'])
        return super().to_internal_value(data=data)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        validated_data.update(
            {
                'caption': InstagramCaption.objects.create(**validated_data.pop('caption')),
                'images': InstagramImages.objects.create(**validated_data.pop('images')),
                'location': InstagramLocation.objects.get_or_create(**validated_data.pop('location'))[0]
            }
        )
        post = InstagramPost.objects.create(**validated_data)
        post.tags.set(tags)

        # Add post to user posts set
        validated_data.get('user').posts.add(post)

        return post

    def update(self, instance, validated_data):
        validated_data.update(
            {
                'caption': InstagramCaption.objects.get_or_create(**validated_data.pop('caption'))[0],
                'images': InstagramImages.objects.get_or_create(**validated_data.pop('images'))[0],
                'location': InstagramLocation.objects.get_or_create(**validated_data.pop('location'))[0]
            }
        )
        info = model_meta.get_field_info(instance)

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
        instance.save()

        return instance
