from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from recipes.models import Tag


class TagViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.model = Tag.objects.create(name='Test tag',
                                        color='#FFFFFF',
                                        slug='test-slug')
        self.model2 = Tag.objects.create(name='Test tag2',
                                        color='#FFFFF1',
                                        slug='test-slug2')



    def test_list_view(self):
        # response = self.client.get('/api/tags/')
        response = self.client.get(reverse('api:tags-list'))
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], self.model.id)
        self.assertEqual(response.data[0]['name'], 'Test tag')
        self.assertEqual(response.data[0]['color'], '#FFFFFF')
        self.assertEqual(response.data[0]['slug'], 'test-slug')
        self.assertEqual(response.data[1]['id'], self.model2.id)

    def test_tag_view(self):
        response = self.client.get(f'/api/tags/{self.model.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.model.id)
        self.assertEqual(response.data['name'], 'Test tag')
        self.assertEqual(response.data['color'], '#FFFFFF')
        self.assertEqual(response.data['slug'], 'test-slug')
        self.assertNotEqual(response.data['id'], self.model2.id)
