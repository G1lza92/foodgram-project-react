from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from recipes.models import Ingredient


class IngredientsViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.model = Ingredient.objects.create(
            name='Test ingredient',
            measurement_unit='Test gramm'
        )
        self.model2 = Ingredient.objects.create(
            name='Test ingredient2',
            measurement_unit='Test gramm2'
        )

    def test_list_view(self):
        response = self.client.get('/api/ingredients/')
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], self.model.id)
        self.assertEqual(response.data[0]['name'], 'Test ingredient')
        self.assertEqual(response.data[0]['measurement_unit'], 'Test gramm')
        self.assertEqual(response.data[1]['id'], self.model2.id)
        self.assertEqual(response.data[1]['name'], 'Test ingredient2')
        self.assertEqual(response.data[1]['measurement_unit'], 'Test gramm2')

    def test_ingredient_view(self):
        response = self.client.get(f'/api/ingredients/{self.model.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.model.id)
        self.assertEqual(response.data['name'], 'Test ingredient')
        self.assertEqual(response.data['measurement_unit'], 'Test gramm')
        self.assertNotEqual(response.data['id'], self.model2.id)

