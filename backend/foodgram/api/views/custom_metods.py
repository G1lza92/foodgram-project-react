from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from recipes.models import Recipe


def custom_post(self, request, id, serializer):
    user = request.user
    data = {'user': user.id, 'recipe': id}
    serializer = serializer(data=data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def custom_delete(self, request, id, model):
    user = request.user
    recipe = get_object_or_404(Recipe, id=id)
    model.objects.all().filter(user=user, recipe=recipe)
    if not model.objects.all().filter(user=user, recipe=recipe).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    model.objects.all().filter(user=user, recipe=recipe).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
