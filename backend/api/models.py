from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.db import models
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class InstagramLocation(models.Model):
    instagram_id = models.IntegerField(unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.TextField()


class InstagramTag(models.Model):
    name = models.TextField(unique=True)


class InstagramImages(models.Model):
    thumbnail_width = models.IntegerField()
    thumbnail_height = models.IntegerField()
    thumbnail_url = models.URLField()
    low_res_width = models.IntegerField()
    low_res_height = models.IntegerField()
    low_res_url = models.URLField()
    standard_res_width = models.IntegerField()
    standard_res_height = models.IntegerField()
    standard_res_url = models.URLField()


class InstagramCaption(models.Model):
    # Base attributes
    instagram_id = models.TextField(unique=True)
    text = models.TextField()
    created_time = models.DateTimeField()

    # Relationship attributes
    user = models.ForeignKey('InstagramUser', on_delete=models.CASCADE)


class InstagramPost(models.Model):
    # Base attributes
    instagram_id = models.TextField(unique=True)
    created_time = models.DateTimeField()
    user_has_liked = models.BooleanField()
    likes = models.IntegerField()
    type = models.TextField()
    link = models.URLField()
    comments = models.IntegerField()

    # Relationship attributes
    user = models.ForeignKey('InstagramUser', on_delete=models.CASCADE)
    tags = models.ManyToManyField(InstagramTag, blank=True)
    location = models.ForeignKey(InstagramLocation, on_delete=models.DO_NOTHING, blank=True, null=True)
    images = models.ForeignKey(InstagramImages, on_delete=models.DO_NOTHING, null=True)
    caption = models.ForeignKey(InstagramCaption, on_delete=models.DO_NOTHING, null=True)

    def delete(self, *args, **kwargs):
        img = self.images
        cap = self.caption
        self.images = None
        self.caption = None
        self.save()

        img.delete()
        cap.delete()
        return super().delete(*args, **kwargs)


class InstagramUser(models.Model):
    # Base attributes
    instagram_id = models.CharField(max_length=20, unique=True)
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
