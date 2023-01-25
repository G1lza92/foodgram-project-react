from rest_framework import views

from api.serializers import FavoriteSerializer
from recipes.models import Favorite
from .custom_metods import custom_delete, custom_post


class FavoriteAPIView(views.APIView):
    """ Класс представления избранного """
    def post(self, request, id):
        return custom_post(self, request, id, FavoriteSerializer)

    def delete(self, request, id):
        return custom_delete(self, request, id, Favorite)
