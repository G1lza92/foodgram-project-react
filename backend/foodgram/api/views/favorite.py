from django.shortcuts import get_object_or_404
from rest_framework import status, views
from rest_framework.response import Response

from api.serializers import FavoriteSerializer
from recipes.models import Favorite, Recipe


class FavoriteAPIView(views.APIView):
    """ Класс представления избранного """
    def post(self, request, id):
        user = request.user
        data = {'user': user.id, 'recipe': id}
        serializer = FavoriteSerializer(data=data,
                                        context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        obj = Favorite.objects.all().filter(user=user, recipe=recipe)
        if not obj:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
