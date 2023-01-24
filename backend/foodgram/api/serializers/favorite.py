from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Favorite, Recipe
from users.models import User


class FavoriteSerializer(serializers.ModelSerializer):
    """ Сериализатор добавления/удаления рецепта в избранное"""
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Favorite
        fields = (
            'user',
            'recipe',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже добавлен в избранное'
            )
        ]
