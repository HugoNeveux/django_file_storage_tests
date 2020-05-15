from django.test import TestCase, Client
from django.contrib.auth.models import User
from Files.models import UserFile
from Auth.models import Profile
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

    def test_files_upload_success(self):
        self.client.login(username='temporary', password='temporary')
        for file in os.listdir('./Files/tests/upload_f'):
            with open(f'./Files/tests/upload_f/{file}') as f:
                response = self.client.post(
                    '/Files/tree/', {'file': f, 'path': ''})
                self.assertEqual(UserFile.objects.filter(
                    name=os.path.basename(f.name)).count(), 1)
                self.assertEqual(response.status_code, 200)
                self.assertJSONEqual(response.content, {'form': True})

    def test_file_too_big(self):
        user = User.objects.get(username='temporary')
        profile = Profile.objects.get(user=user)
        profile.upload_limit = 4 * 1024
        profile.save()
        self.client.login(username='temporary', password='temporary')
        with open(f'./Files/tests/upload_f_err/too_big.txt') as f:
            response = self.client.post(
                '/Files/tree/', {'file': f, 'path': ''}
            )
            self.assertEqual(response.status_code, 400)
            self.assertJSONEqual(response.content, {
                'error': f'Limite de stockage dépassée: le fichier too_big.txt ne peut pas être enregistré.'
            })
            self.assertEqual(UserFile.objects.filter(
                name='too_big.txt').count(), 0)

    def test_file_empty(self):
        self.client.login(username='temporary', password='temporary')
        with open(f'./Files/tests/upload_f_err/empty.txt') as f:
            response = self.client.post(
                '/Files/tree/', {'file': f, 'path': ''}
            )
            self.assertEqual(response.status_code, 400)
            self.assertEqual(UserFile.objects.filter(
                name='empty.txt').count(), 0)
            self.assertJSONEqual(response.content, {
                                 'file': ['The submitted file is empty.']})


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
