from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response


class LikeMixin(generics.GenericAPIView):
    """
    Mixin providing 'like' functionality for a ModelViewSet.
    """

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticatedOrReadOnly])
    def like(self, request, pk=None):
        """
        Putting like for model if user not in many-to-many table or disabling like if user in it.
        Method : POST
        api/v1/<route_name>/<instance_id>/like/
        Headers - {Authorization: JWT <access_token>}
        """
        obj = self.get_object()
        user = request.user
        message, like_counter = obj.like_by_user(user)
        return Response({'status': 'success', 'message': message, 'like_counter': like_counter})


class ViewsCounterMixin(generics.GenericAPIView):
    """
    Mixin providing 'add view' functionality for a ModelViewSet.
    """

    @action(detail=True, methods=['post'], permission_classes=[], url_path='views')
    def views_counter(self, request, pk=None):
        """
        Adding view for model in views field
        Method : POST
        api/v1/<route_name>/<instance_id>/views/
        """
        obj = self.get_object()
        obj.views += 1
        obj.save()
        return Response({'detail': {'views count': obj.views}})
