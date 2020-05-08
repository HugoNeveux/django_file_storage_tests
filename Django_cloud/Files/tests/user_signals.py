from django.test import TestCase
from django.contrib.auth.models import User
import os
import shutil

class UserSignalsTest(TestCase):
    def tearDown(self):
        if os.path.isdir('./media/temporary'):
            shutil.rmtree('./media/temporary')

    def test_user_create(self):
        user = User.objects.create_user(
            'temporary', 'temporary@abcd.com', 'temporary')
        self.assertTrue(os.path.isdir('./media/temporary/files'))
