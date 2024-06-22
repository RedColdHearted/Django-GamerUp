from django.urls import path, include

from rest_framework import routers

from posts.views import PostViewSet, PostPicViewSet, PostCommentViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, 'users')
router.register(r'posts', PostViewSet, 'posts')
router.register(r'pics', PostPicViewSet, 'pics')
router.register(r'comments', PostCommentViewSet, 'comments')


urlpatterns = [
    path('', include(router.urls)),
]
