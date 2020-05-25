from django.test import TestCase, Client
from django.contrib.auth.models import User
from Auth.models import Profile
from django.core.files import File
import os
import shutil


class UploadFileTest(TestCase):
    """
    Tests for file upload
    """
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
        """
        Check if user is redirected when not logged in
        """
        r = self.client.post('/Files/tree/', follow=True)
        self.assertRedirects(r, '/?next=/Files/tree/')

    def test_files_upload_success(self):
        """
        Check if file upload works
        """
        self.client.login(username='temporary', password='temporary')
        for file in os.listdir('./Files/tests/upload_f'):
            with open(f'./Files/tests/upload_f/{file}') as f:
                response = self.client.post(
                    '/Files/tree/', {'file': f, 'path': ''})
                self.assertTrue(os.path.exists(os.path.join('./media/temporary/files/', os.path.basename(f.name))))

    def test_file_too_big(self):
        """
        Check if server rejects upload when file is too big
        """
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
        self.assertFalse(os.path.exists('./media/temporary/files/too_big.txt'))

    def test_file_empty(self):
        """
        Check if server returns an error when file is empty
        """
        self.client.login(username='temporary', password='temporary')
        with open(f'./Files/tests/upload_f_err/empty.txt') as f:
            response = self.client.post(
                '/Files/tree/', {'file': f, 'path': ''}
            )
            self.assertEqual(response.status_code, 400)
            self.assertFalse(os.path.exists('./media/temporary/files/empty.txt'))


class FileListTest(TestCase):
    """
    Test if file listing works
    """
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
        """
        Check if user gets redirected if he isn't logged in
        """
        r = self.client.get('/Files/', follow=True)
        self.assertRedirects(r, '/?next=/Files/')

    def test_call_view_allow_logged_user(self):
        """
        Check if /Files/ works for logged in user
        """
        self.client.login(username='temporary', password='temporary')
        r = self.client.get('/Files/')
        self.assertTemplateUsed('files.html')
        self.assertTrue(r.status_code, 200)

class FileMoveTest(TestCase):
    """
    Test file move view
    """
    def setUp(self):
        """Upload file to move"""
        user = User.objects.create_user(
            'temporary', 'temporary@abcd.com', 'temporary')
        f = File(open('./Files/tests/upload_f/text.txt'))
        self.client.login(username='temporary', password='temporary')
        self.client.post('/Files/tree/', {'file': f, 'path': ''})
        self.client.logout()
        os.mkdir('./media/temporary/files/dir1')
        f.close()

    def test_file_move_success(self):
        """Move file"""
        self.client.login(username='temporary', password='temporary')
        r = self.client.get('/Files/mv/?from=text.txt&to=dir1&redirect=', follow=True)
        self.assertTrue(os.path.exists('./media/temporary/files/dir1/text.txt'))

    def tearDown(self):
        User.objects.filter(username='temporary').delete()
