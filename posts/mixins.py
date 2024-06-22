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
        api/v1/<route_name>/<uuid_of_model>/like/
        Headers - {Authorization: JWT <access_token>}
        """
        obj = self.get_object()
        user = request.user
        if user in obj.liked_by.all():
            obj.liked_by.remove(user)
            obj.like_counter -= 1
            message = 'Like removed'
        else:
            obj.liked_by.add(user)
            obj.like_counter += 1
            message = 'Liked'
        obj.save()
        return Response({'status': 'success', 'message': message, 'like_counter': obj.like_counter})
