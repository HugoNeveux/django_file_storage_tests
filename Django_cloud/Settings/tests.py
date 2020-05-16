from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
import os, shutil

class UserSignalsTest(TestCase):
    def setUp(self):
        User.objects.create_user('temporary', 'temp@abc.fr', 'temporary')

    def test_user_rename(self):
        u = User.objects.get(username='temporary')
        u.username = 'temporary1'
        u.save()
        self.assertTrue(os.path.exists(os.path.join(settings.MEDIA_ROOT, 'temporary1')))

    def tearDown(self):
        paths = ['temporary', 'temporary1']
        for path in paths:
            if os.path.exists(os.path.join(settings.MEDIA_ROOT, path)):
                shutil.rmtree(os.path.join(settings.MEDIA_ROOT, path))
