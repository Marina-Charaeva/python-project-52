from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.messages import get_messages
from task_manager.models import Status

class StatusCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        self.client.login(username='testuser', password='testpassword123')

    def test_status_list_requires_login(self):
        """Незалогиненный пользователь перенаправляется на страницу входа"""
        self.client.logout()
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_status_list(self):
        """Просмотр списка статусов"""
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)

    def test_status_create(self):
        """Создание статуса"""
        response = self.client.post(reverse('status_create'), {
            'name': 'New Status'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='New Status').exists())
        
        # Проверка flash-сообщения
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('successfully' in str(m) for m in messages))

    def test_status_update(self):
        """Редактирование статуса"""
        status = Status.objects.create(name='Old Status')
        response = self.client.post(reverse('status_update', args=[status.id]), {
            'name': 'Updated Status'
        })
        self.assertEqual(response.status_code, 302)
        status.refresh_from_db()
        self.assertEqual(status.name, 'Updated Status')

    def test_status_delete(self):
        """Удаление статуса"""
        status = Status.objects.create(name='To Delete')
        response = self.client.post(reverse('status_delete', args=[status.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(id=status.id).exists())

    def test_status_create_duplicate(self):
        """Проверка уникальности имени"""
        Status.objects.create(name='Existing Status')
        response = self.client.post(reverse('status_create'), {
            'name': 'Existing Status'
        })
        self.assertEqual(response.status_code, 200)  # Форма с ошибкой
        self.assertContains(response, 'already exists')