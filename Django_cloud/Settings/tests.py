from django.test import TestCase
from django.contrib.auth.models import User

class SettingsViewTest(TestCase):
    def setUp(self):
        User.objects.create_user('temporary', 'temp@abc.fr', 'temporary')

    def test_access_no_password(self):
        res = self.client.get('/Settings/', follow=True)
        self.assertRedirects(res, '/?next=/Settings/')

    def test_access_logged_in(self):
        self.client.login(username='temporary', password='temporary')
        res = self.client.get('/Settings/')
        self.assertEqual(res.status_code, 200)

    def tearDown(self):
        User.objects.get(username='temporary').delete()
