from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User

class SetupTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects._create_user(email='test@test.ru', password='123QWE456RTY', is_superuser=True,
                         is_staff=True, is_active=True)

    def setUp(self):
        self.client.login(email='test@test.ru', password='123QWE456RTY')
        response = self.client.post('/api/token/', {"email": "test@test.ru", "password": "123QWE456RTY"})
        if response.status_code == 200:
            self.token = response.data['access']
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        else:
            print(f"Failed to get token: {response.content}")

class UserAPITestCase(SetupTestCase):
    list_url = reverse_lazy('user:user-list')
    create_url = reverse_lazy('user:user-create')

    def test_list_users(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        data = {
            "email": "test2@example.com",
            "password": "secret123",
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='test2@example.com').exists())

    def test_retrieve_user(self):
        url = reverse_lazy('user:user-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        data = {
            "email": "test@example.com",
        }
        url = reverse_lazy('user:user-detail', args=[self.user.id])
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'test@example.com')

    def test_delete_user(self):
        url = reverse_lazy('user:user-delete', args=[self.user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_login(self):
        data = {
            'email': 'test@test.ru',
            'password': '123QWE456RTY'
        }
        url = reverse_lazy('user:token_obtain_pair')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

    def test_unauthenticated_user_access(self):
        self.client.logout()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_str(self):
        expected_str = f'{self.user.email} - {self.user.login_tg}: {self.user.chat_id}'
        self.assertEqual(str(self.user), expected_str)
