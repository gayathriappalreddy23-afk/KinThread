from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthViewsTests(TestCase):
    def test_signup_creates_user_and_redirects_to_login(self):
        response = self.client.post(
            reverse('signup'),
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'password123',
                'confirm_password': 'password123',
            },
        )
        self.assertRedirects(response, f"{reverse('auth_home')}?form=login&email=john@example.com")
        self.assertTrue(User.objects.filter(email='john@example.com').exists())

    def test_login_authenticates_user_and_redirects_to_dashboard(self):
        User.objects.create_user(username='test@example.com', email='test@example.com', password='password123')

        response = self.client.post(
            reverse('login'),
            {
                'email': 'test@example.com',
                'password': 'password123',
            },
        )
        self.assertRedirects(response, reverse('user_profile'))

    def test_logout_clears_session(self):
        user = User.objects.create_user(username='test@example.com', email='test@example.com', password='password123')
        self.client.force_login(user)

        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Logged Out Successfully')

    def test_profile_view_renders_200(self):
        user = User.objects.create_user(username='test@example.com', email='test@example.com', password='password123')
        self.client.force_login(user)
        response = self.client.get(reverse('user_profile'))
        self.assertEqual(response.status_code, 200)

