from django.conf import settings
from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag, TagsInRecipe)


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    """ Отображение модели ингредиентов в админке """
    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = settings.ADMIN_MODEL_EMPTY_VALUE


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """ Отображение модели тегов в админке """
    list_display = (
        'name',
        'color',
        'slug',
    )
    list_filter = (
        'name',
        'slug',
    )
    empty_value_display = settings.ADMIN_MODEL_EMPTY_VALUE


class RecipeTagInline(admin.TabularInline):
    model = TagsInRecipe
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """ Отображение модели рецептов в админке """
    inlines = (RecipeTagInline,)
    list_display = (
        'name',
        'author',
        'pub_date',
        'favorite_recipe'
    )
    list_filter = (
        'name',
        'author',
        'tags',
    )
    empty_value_display = settings.ADMIN_MODEL_EMPTY_VALUE

    def favorite_recipe(self, obj):
        return obj.favorite_recipe.all().count()


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    """ Отображение модели связи рецептов и ингредиентов в админке """
    list_display = (
        'recipe',
        'ingredient',
        'amount',
    )
    list_filter = (
        'recipe',
        'ingredient',
    )
    empty_value_display = settings.ADMIN_MODEL_EMPTY_VALUE


@admin.register(TagsInRecipe)
class TagsInRecipeAdmin(admin.ModelAdmin):
    """ Отображение модели связи рецептов и тегов в админке """
    list_display = (
        'recipe',
        'tags',
    )
    list_filter = (
        'recipe',
        'tags',
    )
    empty_value_display = settings.ADMIN_MODEL_EMPTY_VALUE


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """ Отображение модели избронного в админке """
    list_display = (
        'user',
        'recipe',
    )
    list_filter = (
        'user',
        'recipe',
    )
    empty_value_display = settings.ADMIN_MODEL_EMPTY_VALUE


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """ Отображение модели списка покупок в админке """
    list_display = (
        'user',
        'recipe',
    )
    list_filter = (
        'user',
        'recipe',
    )
    empty_value_display = settings.ADMIN_MODEL_EMPTY_VALUE
