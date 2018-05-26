from django.conf.urls import url
from rest_framework.authtoken import views as drf_views
from backend.api import views
from rest_framework import routers
from django.urls import path, include, re_path


router = routers.DefaultRouter()
router.register(r'igusers', views.InstagramUserViewSet)
router.register(r'igposts', views.InstagramPostsViewSet)

app_name='api'
urlpatterns = [
    url(r'^', include(router.urls)),
    re_path(r'^auth$', drf_views.obtain_auth_token, name='auth'),
]
