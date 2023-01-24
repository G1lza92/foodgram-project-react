from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.filters import RecipeFilter
from api.permissions import IsAuthorOrReadOnly
from api.serializers import RecipeCreateSerializer, RecipeListSerializer
from recipes.models import Recipe


class RecipeViewSet(viewsets.ModelViewSet):
    """ Класс представления рецептов """
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return RecipeListSerializer
        return RecipeCreateSerializer
