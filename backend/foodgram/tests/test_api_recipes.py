import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from recipes.models import Ingredient, Recipe, Tag
from users.models import User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class RecipesViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.model_tag = Tag.objects.create(
            name='Test tag',
            color='#FFFFFF',
            slug='test-slug',
        )
        # tag = Tag.objects.get(name='Test tag')
        self.model_ingredient = Ingredient.objects.create(
            name='Test ingredient',
            measurement_unit='Test gramm'
        )
        # ingredient = Ingredient.objects.get(name='Test ingredient')
        self.user_data = {
            'email': 'test@test.ru',
            'username': 'Test',
            'first_name': 'first_name_test',
            'last_name': 'last_name_test',
            'password': 'testpassword',
        }
        self.client.post('/api/users/', data=self.user_data)
        self.client.post('/api/auth/token/login/', data={
            'email': 'test@test.ru',
            'password': 'testpassword'
        })
        user = User.objects.get(username='Test')
        token = Token.objects.get(user__username=user)
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        self.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        self.model = Recipe.objects.create(
            author=user,
            name='Test',
            image=self.uploaded,
            text='test',
            cooking_time=1
        )
        self.model.tags.add(self.model_tag)
        self.model.ingredients.add(self.model_ingredient)

    def tearDown(self):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_list_view(self):
        response = self.client.get(reverse('/api/recipes/'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], self.model.id)
