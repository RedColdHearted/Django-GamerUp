import os

from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from accounts.serializers import CustomUserCreateSerializer
from posts.serializers import PostSerializer, PostPicSerializer, PostCommentSerializer
from posts.models import UserAccount, Post, PostPic, PostComment
from posts.mixins import LikeMixin
from app.permissions import IsOwnerOrReadOnly
from app.utils import is_not_default_pic


# TODO: update username, documentation ant unittest
class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet
                  ):
    queryset = UserAccount.objects.all()
    serializer_class = CustomUserCreateSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    @action(detail=True, methods=['get', 'post'], url_path='avatar')
    def change_avatar(self, request, pk=None):
        """
        Allow to post user's avatar or get user avatar, if user already have non default avatar, it will be deleted
        api/v1/users/<user_id>/avatar/
        Methods: POST, GET
        if POST:
            Headers - {
                    Content-Type: multipart/form-data; boundary=<calculated when request is sent>
                    Authorization: JWT <access token>
                }
            Body - {
                    **form-data**
                    "avatar": <avatar-file> (type file)
                }
        """
        user = self.get_object()

        if request.method == 'POST':
            if user.id == request.user.id:
                file = request.FILES.get('avatar')
                if not file:
                    return Response({"avatar": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
                old_avatar_path = user.image.path if user.image else None
                old_avatar_name = user.image.name.split('/')[1] if user.image else None

                user.image = file
                user.save()

                if is_not_default_pic(old_avatar_name):
                    os.remove(old_avatar_path)
                return Response({"status": "avatar set"}, status=status.HTTP_200_OK)
            return Response({"avatar": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'GET':
            if not user.image:
                return Response({"avatar": "No image found"}, status=status.HTTP_404_NOT_FOUND)
            response = HttpResponse(user.image, content_type='image/jpeg')
            response['Content-Disposition'] = f'attachment; filename="{user.image.name}"'
            return response


# TODO: unittest
class PostViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet,
                  LikeMixin
                  ):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )

    def create(self, request, *args, **kwargs):
        """
        Creating a post
        Method : Post
        api/v1/posts/
        Headers - {Authorization: JWT <access token>}
        Body - {
                "content": <post text content>,
                "user": "<user id>"
            }
        """
        post_data = request.data
        serializer = PostSerializer(data=post_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Post created', 'data': serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Updating a post
        Method : Put
        api/v1/posts/<uuid of post>/
        Headers - {Authorization: JWT <access token>}
        Body - {
                **new post content**
            }
        """
        post_instance = self.get_object()
        serializer = self.get_serializer(post_instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """
        Deleting a post if requesting user is owner of the post
        Method : Delete
        api/v1/posts/<post_uuid>/
        Headers - {Authorization: JWT <access token>}
        """
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True)
    def filter(self, request, pk=None):
        """
        Get all post of user
        Method : Get
        api/v1/post-comment/<user_id>/filter
        """
        posts = Post.objects.filter(user=pk)
        return Response(PostSerializer(posts, many=True).data)


# TODO: unittest
class PostCommentViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet,
                         LikeMixin
                         ):
    queryset = PostComment.objects.all()
    serializer_class = PostCommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    @action(methods=['get'], detail=True)
    def filter(self, request, pk=None):
        """
        Get all comments for post
        Method : Get
        api/v1/post-comment/<post_uuid>/filter
        """
        user_posts = PostComment.objects.filter(user_post=pk)
        return Response(PostCommentSerializer(user_posts, many=True).data)


# TODO: documentation ant unittest
class PostPicViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = PostPic.objects.all()
    serializer_class = PostPicSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )
