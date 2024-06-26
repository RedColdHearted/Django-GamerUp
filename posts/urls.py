from django.urls import path, include

from rest_framework import routers

from posts.views import PostViewSet, PostImagesViewSet, CommentViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, 'users')
router.register(r'posts', PostViewSet, 'posts')
router.register(r'pics', PostImagesViewSet, 'pics')
router.register(r'comments', CommentViewSet, 'comments')


urlpatterns = [
    path('', include(router.urls)),
]
