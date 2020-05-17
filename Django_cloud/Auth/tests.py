from django.test import TestCase
from django.contrib.auth.models import User
from Auth.models import Profile
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

    def test_user_dirs_creation(self):
        self.assertTrue(os.path.exists(os.path.join(settings.MEDIA_ROOT, 'temporary')))

    def test_user_dir_deleted(self):
        u = User.objects.get(username='temporary')
        u.delete()
        self.assertFalse(os.path.exists(os.path.join(settings.MEDIA_ROOT, 'temporary')))

    def test_user_profile_exists(self):
        u = User.objects.get(username='temporary')
        self.assertEqual(Profile.objects.filter(user=u).count(), 1)

    def tearDown(self):
        paths = ['temporary', 'temporary1']
        for path in paths:
            if os.path.exists(os.path.join(settings.MEDIA_ROOT, path)):
                shutil.rmtree(os.path.join(settings.MEDIA_ROOT, path))
