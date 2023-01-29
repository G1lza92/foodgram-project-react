from django.shortcuts import get_object_or_404
from rest_framework import generics, status, views
from rest_framework.response import Response

from api.serializers import FollowCreateSerializer, FollowListSerializer
from users.models import Follow, User


class FollowAPIView(views.APIView):
    """ Класс создния/удаления подписок """
    def post(self, request, id):
        user = request.user
        data = {'user': user.id, 'following': id}
        serializer = FollowCreateSerializer(data=data,
                                            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        following = get_object_or_404(User, id=id)
        if not Follow.objects.filter(user=user, following=following).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        Follow.objects.filter(user=user, following=following).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowListAPIView(generics.ListAPIView):
    """ Класс представления подписок """
    queryset = Follow.objects.all()
    serializer_class = FollowListSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(following__user=user)
