from django.contrib.auth.models import User
from django.test import TestCase


class GuifiAdminTest(TestCase):
    
    def test_admin_device(self):
        user = User.objects.create_superuser('admin', 'admin@example.org', 'admin')
        
        logged_in = self.client.login(username='admin', password='admin')
        self.assertTrue(logged_in)
        
        response = self.client.get('/admin/guifi/device/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('device', response.content)
