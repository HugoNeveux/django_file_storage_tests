from django.test import TestCase
from django.contrib.auth.models import User

class SettingsViewTest(TestCase):
    """
    Tests the only settings view
    """
    def setUp(self):
        User.objects.create_user('temporary', 'temp@abc.fr', 'temporary')

    def test_access_no_password(self):
        """
        Check if user is redirected if not logged in
        """
        res = self.client.get('/Settings/', follow=True)
        self.assertRedirects(res, '/?next=/Settings/')

    def test_access_logged_in(self):
        """
        Check if page works well if user is logged in
        """
        self.client.login(username='temporary', password='temporary')
        res = self.client.get('/Settings/')
        self.assertEqual(res.status_code, 200)

    def tearDown(self):
        User.objects.get(username='temporary').delete()
