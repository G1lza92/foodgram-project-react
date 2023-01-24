import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка данный в БД из csv файлов'

    def handle(self, *args, **options):
        with open('data/ingredients.json', 'rb') as file:
            data = json.load(file)
            for value in data:
                ingredient = Ingredient()
                ingredient.name = value["name"]
                ingredient.measurement_unit = value["measurement_unit"]
                ingredient.save()
            print('Ингредиенты загружены')
