from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from posts.views import UserViewSet, ProfilePicViewSet, PostViewSet, PostPicViewSet, PostCommentViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfilePicViewSet)
router.register(r'posts', PostViewSet)
router.register(r'post-pics', PostPicViewSet)
router.register(r'post-coment', PostCommentViewSet)


urlpatterns = [
    path('/', include(router.urls)),
]