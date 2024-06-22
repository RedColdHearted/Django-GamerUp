from django.urls import path, include

from rest_framework import routers

from posts.views import PostViewSet, PostPicViewSet, PostCommentViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'post-pics', PostPicViewSet)
router.register(r'post-comment', PostCommentViewSet)


urlpatterns = [
    path('/', include(router.urls)),
]
