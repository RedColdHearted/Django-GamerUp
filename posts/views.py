from rest_framework.decorators import action
from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from django.http import HttpResponse

from accounts.serializers import CustomUserCreateSerializer
from posts.serializers import PostSerializer, PostPicSerializer, PostCommentSerializer, UsernameChangeSerializer
from posts.models import UserAccount, Post, PostImage, Comment
from posts.mixins import LikeMixin, ViewsCounterMixin
from app.permissions import IsOwnerOrReadOnly


# TODO: unittests
class UserViewSet(mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet
                  ):
    queryset = UserAccount.objects.all()
    serializer_class = CustomUserCreateSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    # TODO: documentation
    @action(detail=True, methods=['post'], url_path='username')
    def change_username(self, request, pk=None):
        """
        Update a model instance.
        """
        user = self.get_object()

        if user.id == request.user.id:
            serializer = UsernameChangeSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                username = serializer.validated_data['username']
                try:
                    user.set_username(username)
                    return Response({'detail': f'new username {username}'}, status=status.HTTP_200_OK)
                except Exception as err:
                    return Response({'error': err},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)

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
                    return Response({"detail": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
                user.set_image(file)
                return Response({"detail": "avatar set"}, status=status.HTTP_200_OK)
            return Response({"detail": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'GET':
            image = user.get_image()
            if not image:
                return Response({"detail": "No image found"}, status=status.HTTP_404_NOT_FOUND)
            response = HttpResponse(image, content_type='image/jpeg')
            response['Content-Disposition'] = f'attachment; filename="{image.name}"'
            return response


class PostViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet,
                  ViewsCounterMixin,
                  LikeMixin
                  ):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def create(self, request, *args, **kwargs):
        """
        Creating a post
        Method : Post
        api/v1/posts/
        Headers - {Authorization: JWT <access token>}
        Body - {
                "title": <post text title>,
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
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True)
    def get_by_user(self, request, pk=None):
        """
        Get all post of user
        Method : Get
        api/v1/posts/<user_id>/get_by_user
        """
        posts = Post.objects.filter(user=pk)
        return Response(PostSerializer(posts, many=True).data)


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet,
                     ViewsCounterMixin,
                     LikeMixin
                     ):
    # FIXME: change update mixin to not allow edit PostComment.user and PostComment.user_post fields
    queryset = Comment.objects.all()
    serializer_class = PostCommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    @action(methods=['get'], detail=True)
    def get_by_post(self, request, pk=None):
        """
        Get all comments for post
        Method : Get
        api/v1/comments/<post_uuid>/get_by_post
        """
        comments = Comment.objects.filter(user_post=pk)
        return Response(PostCommentSerializer(comments, many=True).data)


# TODO: documentation, unittests
class PostImagesViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = PostImage.objects.all()
    serializer_class = PostPicSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
