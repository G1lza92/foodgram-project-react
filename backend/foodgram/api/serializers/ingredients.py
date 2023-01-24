from rest_framework import serializers

from recipes.models import Ingredient, IngredientInRecipe


class IngredientListSerializer(serializers.ModelSerializer):
    """ Cериализатор ингридиентов в рецепте """
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class IngredientInRecipeListSerializer(serializers.ModelSerializer):
    """ Сериализатор ингредиентов в рецепте """
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientInRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """ Cериализатор создания ингредиентов в рецепте """
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient'
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = (
            'id',
            'amount',
        )
