from django.db.models import Sum
from django.http import HttpResponse
from rest_framework import status, views
from rest_framework.response import Response

from api.serializers import ShoppingCartSerializer
from recipes.models import ShoppingCart

from .custom_metods import custom_delete, custom_post


class ShoppingCartAPIView(views.APIView):
    """ Класс представления корзины """
    def post(self, request, id):
        return custom_post(self, request, id, ShoppingCartSerializer)

    def delete(self, request, id):
        return custom_delete(self, request, id, ShoppingCart)


class ShoppingCartGetAPIView(views.APIView):
    """ Класс для скачивания списка покупок """
    def get(self, request):
        user = request.user
        if not user.shoppingcart.exists():
            return Response(
                'В корзине нет товаров', status=status.HTTP_400_BAD_REQUEST
            )
        ingredient_name = 'recipe__recipe__ingredient__name'
        ingredient_unit = 'recipe__recipe__ingredient__measurement_unit'
        recipe_amount = 'recipe__recipe__amount'
        amount_sum = 'recipe__recipe__amount__sum'
        cart = user.shoppingcart.select_related('recipe').values(
            ingredient_name, ingredient_unit).annotate(
            Sum(recipe_amount)).order_by(ingredient_name)
        text = []
        for item in cart:
            text += (
                f'{item[ingredient_name]} ({item[ingredient_unit]})'
                f' — {item[amount_sum]}\n'
            )
        response = HttpResponse(text, content_type='text/plain')
        filename = f'{user.username}_shopping_list.csv'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
