from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from users.models import User


class UserViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'test@test.ru',
            'username': 'Test',
            'first_name': 'first_name_test',
            'last_name': 'last_name_test',
            'password': 'testpassword',
        }

    def test_user_create(self):
        response = self.client.post('/api/users/', data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username='Test')
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.__str__(), user.username)

    def test_user_authentication(self):
        self.client.post('/api/users/', data=self.user_data)

        response = self.client.post('/api/auth/token/login/', data={
            'email': 'test@test.ru',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_list_view(self):
        self.client.post('/api/users/', data=self.user_data)
        response = self.client.get('/api/users/')
        user = User.objects.get(username='Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['username'],
                         user.username)

    def test_unauthorized_access(self):
        response = self.client.get('/api/users/1/')
        self.assertEqual(response.status_code, 401)

    def test_user_profile_view(self):
        self.client.post('/api/users/', data=self.user_data)
        self.client.post('/api/auth/token/login/', data={
            'email': 'test@test.ru',
            'password': 'testpassword'
        })
        user = User.objects.get(username='Test')
        token = Token.objects.get(user__username=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.get(f'/api/users/{user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
