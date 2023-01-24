from djoser import utils
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from users.models import User


class UserViewSetTestCase(APITestCase):
    @classmethod
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='test@test.ru',
            username='Test',
            first_name='first_name_test',
            last_name='last_name_test',
            password='testpassword',
        )
        self.user2 = User.objects.create_user(
            email='test2@test.ru',
            username='Test2',
            first_name='first_name_test2',
            last_name='last_name_test2',
            password='testpassword',
        )
        self.client1 = APIClient()
        # self.client1.force_authenticate(user=self.user1)
        # token = utils.login(self.client1, self.user1)
        # self.client1.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.client2 = APIClient()
        self.client2.force_authenticate(user=self.user2)

    def test_list_view(self):
        response = self.client1.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['id'], self.user1.id)
        self.assertEqual(response.data['results'][0]['username'], 'Test')
        self.assertEqual(response.data['results'][0]['email'], 'test@test.ru')
        self.assertEqual(response.data['results'][0]['is_subscribed'], False)
        self.assertEqual(response.data['results'][1]['id'], self.user2.id)
        self.assertEqual(response.data['results'][1]['username'], 'Test2')
        self.assertEqual(response.data['results'][1]['email'], 'test2@test.ru')

    # def test_user_view(self):
    #     response = self.client1.post(
    #         '/api/auth/token/login/',
    #         {'email': 'test@test.ru', 'password': 'testpassword'}
    #     )
    #     # self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     token = response.data['auth_token']
    #     headers = {'Authorization': 'Token ' + token, 'Accept': 'application/json'}
    #     print(headers)
    #     response = self.client1.get('/api/users/1', headers=headers)
    #     print(dir(response))
    #     print(response.content)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data['results']), 1)
    #     self.assertEqual(response.data['results'][0]['id'], self.user1.id)
    #     self.assertEqual(response.data['results'][0]['username'], 'Test')
    #     self.assertEqual(response.data['results'][0]['email'], 'test@test.ru')
    #     self.assertEqual(response.data['results'][0]['username'], 'Test')
    #     self.assertEqual(response.data['results'][1]['username'], 'Test2')
