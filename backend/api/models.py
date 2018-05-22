from django.conf import settings
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class InstagramPost(models.Model):
    # Base attributes
    id = models.TextField(primary_key=True)
    created_time = models.DateTimeField()
    user_has_liked = models.BooleanField()
    likes = models.IntegerField()
    type = models.TextField()
    link = models.URLField()

    # Relationship attributes
    user = models.ForeignKey('InstagramUser', on_delete=models.DO_NOTHING)


class InstagramUser(models.Model):
    # Base attributes
    id = models.CharField(max_length=20, primary_key=True)
    username = models.TextField()
    profile_picture = models.TextField()
    full_name = models.TextField()
    bio = models.TextField()
    website = models.URLField(blank=True)
    is_business = models.BooleanField()
    counts_media = models.IntegerField()
    counts_follows = models.IntegerField()
    counts_followed_by = models.IntegerField()

    # Relationship attributes
    posts = models.ManyToManyField(InstagramPost)

# class InstagramImages(models.Model):
#     thumbnail_width = models.IntegerField()
#     thumbnail_height = models.IntegerField()
#     thumbnail_url = models.URLField()
#     low_res_width = models.IntegerField()
#     low_res_height = models.IntegerField()
#     low_res_url = models.URLField()
#     standard_res_width = models.IntegerField()
#     standard_res_height = models.IntegerField()
#     standard_res_url = models.URLField()
#
#
# class InstagramTag(models.Model):
#     name = models.TextField()
#
#
# class InstagramLocation(models.Model):
#     id = models.IntegerField(primary_key=True)
#     latitude = models.FloatField()
#     longitude = models.FloatField()
#     name = models.TextField()
#
#
# class InstagramPost(models.Model):
#     # Base attributes
#     id = models.TextField(primary_key=True)
#     created_time = models.DateTimeField()
#     user_has_liked = models.BooleanField()
#     likes = models.IntegerField()
#     type = models.TextField()
#     link = models.URLField()
#
#     # Relationship attributes
#     user = models.ForeignKey('InstagramUser', on_delete=models.DO_NOTHING)
#     images = models.ForeignKey(InstagramImages, on_delete=models.CASCADE)
#     tags = models.ManyToManyField(InstagramTag, blank=True)
#     location = models.ForeignKey(InstagramLocation, on_delete=models.DO_NOTHING, blank=True)
#     users_in_photo = models.ManyToManyField('InstagramUser', related_name='users_in_photo', blank=True)
#
#
# class InstagramUser(models.Model):
#     # Base attributes
#     id = models.CharField(max_length=20, primary_key=True)
#     username = models.TextField()
#     profile_picture = models.TextField()
#     full_name = models.TextField()
#     bio = models.TextField()
#     website = models.URLField(blank=True)
#     is_business = models.BooleanField()
#     counts_media = models.IntegerField()
#     counts_follows = models.IntegerField()
#     counts_followed_by = models.IntegerField()
#
#     # Relationship attributes
#     posts = models.ManyToManyField(InstagramPost)
