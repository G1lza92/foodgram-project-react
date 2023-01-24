from django.urls import include, path
from rest_framework import routers

from .views import (FavoriteAPIView, FollowAPIView, FollowListAPIView,
                    IngredientViewSet, RecipeViewSet, ShoppingCartAPIView,
                    ShoppingCartGetAPIView, TagViewSet)

app_name = 'api'

router = routers.DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path(
        'users/subscriptions/',
        FollowListAPIView.as_view(),
        name='subscriptions'
    ),
    path('users/<id>/subscribe/', FollowAPIView.as_view(), name='subscribe'),
    path(
        "recipes/<int:id>/favorite/",
        FavoriteAPIView.as_view(),
        name="favorite",
    ),
    path(
        "recipes/<int:id>/shopping_cart/",
        ShoppingCartAPIView.as_view(),
        name="shopping_cart",
    ),
    path(
        "recipes/download_shopping_cart/",
        ShoppingCartGetAPIView.as_view(),
        name="download_shopping_cart",
    ),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
