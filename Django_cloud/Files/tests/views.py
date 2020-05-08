from django.test import TestCase, Client
from django.contrib.auth.models import User
from Files.models import UserFile
import os
import shutil


class UploadFileTest(TestCase):
    def setUp(self):
        if not os.path.isdir('./media'):
            os.mkdir('./media')
        if os.path.isdir('./media/temporary'):
            shutil.rmtree('./media/temporary')
        user = User.objects.create_user(
            'temporary', 'temporary@abcd.com', 'temporary')

    def tearDown(self):
        if os.path.isdir('./media/temporary'):
            shutil.rmtree('./media/temporary')

    def test_no_login_redirect(self):
        r = self.client.post('/Files/tree/', follow=True)
        self.assertRedirects(r, '/?next=/Files/tree/')

    # def test_files_upload_success(self):
    #     self.client.login(username='temporary', password='temporary')
    #     for file in os.listdir('./Files/tests/upload_f'):
    #         with open(f'./Files/tests/upload_f/{file}') as f:
    #             response = self.client.post(
    #                 '/Files/tree/', {'name': f.name, 'file': f})
    #             print(UserFile.objects.all())
    #             self.assertEqual(UserFile.objects.filter(name=f.name).count(), 1)

    # NOTE: above test doesn't work as expected and needs fixing


class FileListTest(TestCase):
    def setUp(self):
        if not os.path.isdir('./media'):
            os.mkdir('./media')
        if os.path.isdir('./media/temporary'):
            shutil.rmtree('./media/temporary')
        user = User.objects.create_user(
            'temporary', 'temporary@abcd.com', 'temporary')

    def tearDown(self):
        if os.path.isdir('./media/temporary'):
            shutil.rmtree('./media/temporary')

    def test_call_view_deny_anonymous(self):
        r = self.client.get('/Files/', follow=True)
        self.assertRedirects(r, '/?next=/Files/')

    def test_call_view_allow_logged_user(self):
        self.client.login(username='temporary', password='temporary')
        r = self.client.get('/Files/')
        self.assertTemplateUsed('files.html')
