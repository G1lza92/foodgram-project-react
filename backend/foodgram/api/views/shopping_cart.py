import csv

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, views
from rest_framework.response import Response

from api.serializers import ShoppingCartSerializer
from recipes.models import Recipe, ShoppingCart


class ShoppingCartAPIView(views.APIView):
    """ Класс представления корзины """

    def post(self, request, id):
        user = request.user
        data = {'user': user.id, 'recipe': id}
        serializer = ShoppingCartSerializer(data=data,
                                        context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        obj = ShoppingCart.objects.all().filter(user=user, recipe=recipe)
        if not obj:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartGetAPIView(views.APIView):
    """ Класс для скачивания списка покупок """
    def get(self, request):
        user = request.user
        if not user.shoppingcart.exists():
            return Response(
                'В корзине нет товаров', status=status.HTTP_400_BAD_REQUEST
            )

        ingredients = ShoppingCart.objects.filter(user=user.id).values_list(
            'recipe__ingredients__name',
            'recipe__ingredients__measurement_unit',
            'recipe__ingredients__ingredient__amount',
        )

        shopping_cart = {}
        for ingredient in ingredients:
            name = ingredient[0]
            if name not in shopping_cart:
                shopping_cart[name] = {
                    'measurement_unit': ingredient[1],
                    'amount': ingredient[2]
                }
            else:
                shopping_cart[name]['amount'] += ingredient[2]

        response = HttpResponse(content_type='text/csv')
        filename = f'{user.username}_shopping_list.csv'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        write = csv.writer(response)
        write.writerow(['Ingredient', 'Amount', 'Measure unit'])
        for item in shopping_cart:
            write.writerow([
                item,
                shopping_cart[item]['amount'],
                shopping_cart[item]['measurement_unit']
            ])
        return response
