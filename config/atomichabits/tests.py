from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TestCase
from atomichabits.models import Habit
from user.models import User


class TestHabitViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(email='test@test.ru', is_superuser=True, is_staff=True, is_active=True, password = '12345')
        cls.habit = Habit.objects.create(user=cls.user, place='Home', action='Run')

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_habit_list(self):
        response = self.client.get(reverse('atomichabits:habit_list_create'))
        self.assertEqual(response.status_code, 200)

    def test_habit_create(self):
        data = {
            'place': 'Home',
            'action': 'Read a book'
        }
        response = self.client.post(reverse('atomichabits:habit_list_create'), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Habit.objects.count(), 2)

    def test_habit_detail(self):
        response = self.client.get(reverse('atomichabits:habit_retrieve_update_destroy', args=[self.habit.id]))
        self.assertEqual(response.status_code, 200)

    def test_update_habit(self):
        data = {'place': 'Park'}
        response = self.client.patch(reverse('atomichabits:habit_retrieve_update_destroy', args=[self.habit.id]), data)
        self.assertEqual(response.status_code, 200)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.place, 'Park')

    def test_delete_habit(self):
        response = self.client.delete(reverse('atomichabits:habit_retrieve_update_destroy', args=[self.habit.id]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Habit.objects.count(), 0)
