from django.contrib.auth import get_user_model
from django.test import TestCase


class DashboardViewTests(TestCase):
    def test_dashboard_renders_clean_dashboard_layout(self):
        user = get_user_model().objects.create_user(username='demo', password='demo123')
        self.client.force_login(user)

        response = self.client.get('/dashboard/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'dashboard-shell')
        self.assertContains(response, 'section-heading')
