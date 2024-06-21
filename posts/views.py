from rest_framework.decorators import action
from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from accounts.serializers import CustomUserCreateSerializer
from posts.serializers import ProfilePicSerializer, PostSerializer, PostPicSerializer, PostCommentSerializer
from posts.models import UserAccount, ProfilePic, Post, PostPic, PostComment
from app.permissions import IsOwnerOrReadOnly


# TODO: этот viewset нужен? подумать
class UserViewSet(mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = CustomUserCreateSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


# TODO: сделать документацию и подробные методы
class ProfilePicViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = ProfilePic.objects.all()
    serializer_class = ProfilePicSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class PostViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
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
        api/v1/posts/<uuid of post>/
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
        api/v1/post-comment/<user id>/filter
        """
        posts = Post.objects.filter(user=pk)
        return Response(PostSerializer(posts, many=True).data)


# TODO: сделать документацию и подробные методы
class PostPicViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = PostPic.objects.all()
    serializer_class = PostPicSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )


class PostCommentViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    queryset = PostComment.objects.all()
    serializer_class = PostCommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticatedOrReadOnly])
    def like(self, request, pk=None):
        """
        Putting like for comment if user not in many-to-many table or disabling like if user in it
        Method : Post
        api/v1/post-comment/<uuid of post comment>/like
        Headers - {Authorization: JWT <access token>}
        """
        comment = self.get_object()
        user = request.user
        if user in comment.liked_by.all():
            comment.liked_by.remove(user)
            comment.like_counter -= 1
            message = 'Like removed'
        else:
            comment.liked_by.add(user)
            comment.like_counter += 1
            message = 'Liked'
        comment.save()
        return Response({'status': 'success', 'message': message, 'like_counter': comment.like_counter})

    @action(methods=['get'], detail=True)
    def filter(self, request, pk=None):
        """
        Get all comments for post
        Method : Get
        api/v1/post-comment/<uuid of post>/filter
        """
        user_posts = PostComment.objects.filter(user_post=pk)
        return Response(PostCommentSerializer(user_posts, many=True).data)
