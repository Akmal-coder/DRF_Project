from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User, Subscription
from materials.models import Course, Lesson


class MainTests(TestCase):
    """Основные тесты проекта"""

    def setUp(self):
        """Подготовка данных"""
        # Создаем пользователя
        self.user = User.objects.create_user(
            email='user@test.com',
            password='12345'
        )

        # Создаем курс
        self.course = Course.objects.create(
            title='Тестовый курс',
            owner=self.user
        )

        # Создаем урок
        self.lesson = Lesson.objects.create(
            title='Тестовый урок',
            course=self.course,
            owner=self.user,
            video_link='https://www.youtube.com/watch?v=123'
        )

        # Настраиваем клиент
        self.client = APIClient()

    def test_01_get_lessons(self):
        """Тест 1: Получение списка уроков"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/lessons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_02_create_lesson(self):
        """Тест 2: Создание урока"""
        self.client.force_authenticate(user=self.user)

        data = {
            'title': 'Новый урок',
            'course': self.course.id,
            'video_link': 'https://www.youtube.com/watch?v=456'
        }

        response = self.client.post('/api/lessons/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_03_create_lesson_invalid_link(self):
        """Тест 3: Создание урока с плохой ссылкой"""
        self.client.force_authenticate(user=self.user)

        data = {
            'title': 'Новый урок',
            'course': self.course.id,
            'video_link': 'https://vimeo.com/123'
        }

        response = self.client.post('/api/lessons/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_04_subscription(self):
        """Тест 4: Подписка на курс"""
        self.client.force_authenticate(user=self.user)

        # Подписываемся
        data = {'course_id': self.course.id}
        response = self.client.post('/api/subscription/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Подписка добавлена')

        # Проверяем, что подписка есть
        self.assertTrue(
            Subscription.objects.filter(
                user=self.user,
                course=self.course
            ).exists()
        )

    def test_05_unsubscribe(self):
        """Тест 5: Отписка от курса"""

        Subscription.objects.create(user=self.user, course=self.course)

        self.client.force_authenticate(user=self.user)

        # Отписываемся
        data = {'course_id': self.course.id}
        response = self.client.post('/api/subscription/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')

        # Проверяем, что подписки нет
        self.assertFalse(
            Subscription.objects.filter(
                user=self.user,
                course=self.course
            ).exists()
        )