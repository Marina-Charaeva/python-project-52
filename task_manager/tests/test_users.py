
import pytest
from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class UserCrudAuthTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создадим одного пользователя заранее для тестов на редактирование/удаление
        cls.user = User.objects.create_user(
            username='existing_user',
            password='StrongPass123!',
            first_name='Иван',
            last_name='Иванов'
        )
        # Второй пользователь, чтобы проверить запрет на редактирование чужого
        cls.other_user = User.objects.create_user(
            username='other_user',
            password='StrongPass123!',
            first_name='Петр',
            last_name='Петров'
        )

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('user-create')
        self.users_url = reverse('users')
        self.login_url = reverse('login')

    # --- C: Create (регистрация) ---
    def test_register_success_and_redirect_to_login(self):
        response = self.client.post(self.register_url, {
            'username': 'new_user',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'first_name': 'Алексей',
            'last_name': 'Алексеев',
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.login_url)
        self.assertTrue(User.objects.filter(username='new_user').exists())

        # Проверка flash-сообщения
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn('Пользователь успешно зарегистрирован', str(messages[0]))

    def test_register_duplicate_username_shows_error(self):
        # Регистрируем сначала
        self.client.post(self.register_url, {
            'username': 'dup_user',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        # Пытаемся снова
        response = self.client.post(self.register_url, {
            'username': 'dup_user',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'уже существует')

    # --- R: Read (список пользователей) ---
    def test_users_list_available_without_login(self):
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('users', response.context)

    # --- U: Update (обновление) ---
    def test_update_own_profile_success(self):
        # Логин
        self.client.login(username='existing_user', password='StrongPass123!')
        update_url = reverse('user-update', kwargs={'pk': self.user.pk})

        response = self.client.post(update_url, {
            'first_name': 'Иван Обновленный',
            'last_name': 'Иванов Обновленный',
            'username': 'existing_user',
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.users_url)

        updated_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(updated_user.first_name, 'Иван Обновленный')

        messages_list = list(response.context['messages'])
        self.assertIn('Пользователь успешно изменен', str(messages_list[0]))

    def test_update_other_user_denied(self):
        self.client.login(username='existing_user', password='StrongPass123!')
        update_url = reverse('user-update', kwargs={'pk': self.other_user.pk})

        response = self.client.post(update_url, {
            'first_name': 'Злой хакер',
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.users_url)

        messages_list = list(response.context['messages'])
        self.assertIn('У вас нет прав для изменения', str(messages_list[0]))

        # Данные другого пользователя не должны измениться
        self.other_user.refresh_from_db()
        self.assertNotEqual(self.other_user.first_name, 'Злой хакер')

    # --- D: Delete (удаление) ---
    def test_delete_own_account_success(self):
        self.client.login(username='existing_user', password='StrongPass123!')
        delete_url = reverse('user-delete', kwargs={'pk': self.user.pk})

        response = self.client.post(delete_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.users_url)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

        messages_list = list(response.context['messages'])
        self.assertIn('Пользователь успешно удален', str(messages_list[0]))

    def test_delete_other_user_denied(self):
        self.client.login(username='existing_user', password='StrongPass123!')
        delete_url = reverse('user-delete', kwargs={'pk': self.other_user.pk})

        response = self.client.post(delete_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.users_url)

        messages_list = list(response.context['messages'])
        self.assertIn('У вас нет прав для удаления', str(messages_list[0]))

        # Другой пользователь должен остаться
        self.assertTrue(User.objects.filter(pk=self.other_user.pk).exists())

    # --- Auth (вход/выход) ---
    def test_login_success_redirects_to_index(self):
        index_url = reverse('index')
        response = self.client.post(self.login_url, {
            'username': 'existing_user',
            'password': 'StrongPass123!',
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, index_url)

        messages_list = list(response.context['messages'])
        self.assertIn('Вы залогинены', str(messages_list[0]))

    def test_logout_success_redirects_to_index(self):
        self.client.login(username='existing_user', password='StrongPass123!')
        logout_url = reverse('logout')
        index_url = reverse('index')

        response = self.client.post(logout_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, index_url)

        messages_list = list(response.context['messages'])
        self.assertFalse(response.wsgi_request.user.is_authenticated)