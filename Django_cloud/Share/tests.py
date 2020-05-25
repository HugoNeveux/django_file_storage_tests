from django.test import TestCase
from Share.models import ShareLink
from django.contrib.auth.models import User
from django.http import FileResponse
import os, shutil

class TestShare(TestCase):
    """
    Test for ShareLink creation
    """
    def setUp(self):
        User.objects.create_user(
            'temporary', 'temporary@abcd.com', 'temporary')
        os.mkdir('./media/temporary/files/test_dir')
        shutil.copyfile('./Files/tests/upload_f/text.txt',
                        './media/temporary/files/test_dir/text.txt')

    def tearDown(self):
        User.objects.get(username='temporary').delete()


    def test_create_sharelink_file_success(self):
        """
        Sharelink creation test for a single file
        """
        self.client.login(username='temporary', password='temporary')
        resp = self.client.get('/Share/create/test_dir/text.txt/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(ShareLink.objects.filter(file_path='test_dir/text.txt').count(), 1)

    def test_create_sharelink_dir_success(self):
        """
        ShareLink creation test for a directory
        """
        self.client.login(username='temporary', password='temporary')
        resp = self.client.get('/Share/create/test_dir/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(ShareLink.objects.filter(file_path='test_dir').count(), 1)

    def test_create_sharelink_fail(self):
        """
        ShareLink creation attempt for non-existing file
        """
        self.client.login(username='temporary', password='temporary')
        resp = self.client.get('/Share/create/non/existent/file/')
        self.assertEqual(resp.status_code, 404)

    def test_create_sharelink_non_logged_in(self):
        """
        Attempt to create a share link with not authenticated user
        """
        resp = self.client.get('/Share/create/test_dir/text.txt/', follow=True)
        self.assertRedirects(resp, '/?next=/Share/create/test_dir/text.txt/')

class TestSharedDownload(TestCase):
    """
    Test the download of shared files
    """
    def setUp(self):
        user = User.objects.create_user(
            'temporary', 'temporary@abcd.com', 'temporary')
        os.mkdir('./media/temporary/files/test_dir')
        shutil.copyfile('./Files/tests/upload_f/text.txt',
                        './media/temporary/files/test_dir/text.txt')
        ShareLink(link="LinkToSharedFile", creator=user, file_path='test_dir/text.txt').save()
        ShareLink(link="LinkToSharedDir1", creator=user, file_path='test_dir').save()

    def test_download_file(self):
        """
        Download of a single file
        """
        resp = self.client.get('/Share/s/LinkToSharedFile/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(isinstance(resp, FileResponse))

    def test_download_dir(self):
        """
        Download a directory
        """
        resp = self.client.get('/Share/s/LinkToSharedDir1/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['Content-Type'], 'application/x-zip-compressed')

    def test_download_wrong_link(self):
        """
        Check if user gets 404 when using non existing link
        """
        resp = self.client.get('/Share/s/NonExistingLink/')
        self.assertEqual(resp.status_code, 404)

    def test_file_deleted_fail(self):
        """
        Check if user gets 404 when trying to access moved or deleted file
        """
        os.remove('./media/temporary/files/test_dir/text.txt')
        resp = self.client.get('/Share/s/LinkToSharedFile/')
        self.assertEqual(resp.status_code, 404)

    def test_dir_deleted_fail(self):
        """
        Check if user gets 404 when trying to access moved or deleted dir
        """
        shutil.rmtree('./media/temporary/files/test_dir/')
        resp = self.client.get('/Shre/s/LinkToSharedDir1/')
        self.assertEqual(resp.status_code, 404)

    def tearDown(self):
        User.objects.get(username='temporary').delete()
