from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (Favorite, IngredientInRecipe, Recipe, ShoppingCart,
                            Tag)
from users.serializers import UserListSerializer

from .ingredients import (IngredientInRecipeListSerializer,
                          IngredientInRecipeSerializer)
from .tags import TagSerializer


class BaseRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'is_favorited',
            'is_in_shopping_cart',
        )

    def get_is_favorited(self, obj):
        """ Функция добавления пользователем рецепта в избранное """
        user = self.context['request'].user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user.id, recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        """ Функция добавления пользователем рецепта в лист покупок """
        user = self.context['request'].user
        if user.is_authenticated:
            return ShoppingCart.objects.filter(
                user=user.id, recipe=obj).exists()
        return False


class RecipeListSerializer(BaseRecipeSerializer):
    """ Сериализатор рецептов """
    author = UserListSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = IngredientInRecipeListSerializer(
        many=True,
        required=True,
        source='recipe'
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'image',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'text',
            'cooking_time',
        )


class RecipeCreateSerializer(BaseRecipeSerializer):
    """ Сериализатор создания рецептов """
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = IngredientInRecipeSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'ingredients',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    def create_ingredients(self, ingredients, recipe):
        """ Функция создания пользователем ингредиента в рецепте """
        for ingredient in ingredients:
            IngredientInRecipe.objects.update_or_create(
                recipe=recipe,
                ingredient=ingredient['ingredient'],
                amount=ingredient['amount'],
            )

    def create(self, validated_data):
        author = self.context['request'].user
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            instance.ingredients.clear()
            self.create_ingredients(ingredients, instance)
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            instance.tags.clear()
            instance.tags.set(tags)
        super().update(instance, validated_data)
        return instance

    def validate(self, data):
        ingredients = data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError(
                'Необходимо выбрать хотя бы один ингредиент')
        if [item for item in ingredients if item['amount'] < 1]:
            raise serializers.ValidationError(
                'Минимальное количество ингредиента 1')
        for ingredient in ingredients:
            if ingredients.count(ingredient) > 1:
                raise serializers.ValidationError(
                    'Ингредиенты не должны повторятся')
        tags = data.get('tags')
        for tag in tags:
            if tags.count(tag) > 1:
                raise serializers.ValidationError('Тэги не должны повторяться')
        cooking_time = data.get('cooking_time')
        if cooking_time <= 0:
            raise serializers.ValidationError(
                'Время готовки должно быть больше 0')
        return data

    def to_representation(self, instance):
        return RecipeListSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data
