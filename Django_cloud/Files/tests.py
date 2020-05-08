from django.test import TestCase
from .file_utils import format_bytes, recursive_file_list
import shutil, os, tempfile

class FormatBytesTest(TestCase):
    """Testing format_bytes function"""
    def test_b(self):
        self.assertEqual(format_bytes(0), '0B')
        self.assertEqual(format_bytes(1000), '1000B')
    def test_kb(self):
        self.assertEqual(format_bytes(1024), '1.0KB')
        self.assertEqual(format_bytes(1024 + 512), '1.5KB')
    def test_mb(self):
        self.assertEqual(format_bytes(1024**2), '1.0MB')
        self.assertEqual(format_bytes(1024**2 + (1024**2 / 2)), '1.5MB')
    def test_gb(self):
        self.assertEqual(format_bytes(1024**3), '1.0GB')
        self.assertEqual(format_bytes(1024**3 + (1024**3 / 2)), '1.5GB')
    def test_tb(self):
        self.assertEqual(format_bytes(1024**4), '1.0TB')
        self.assertEqual(format_bytes(1024**4 + (1024**4 / 2)), '1.5TB')

class FileListTest(TestCase):
    """Testing recursive_file_list function"""
    def setUp(self):
        try:
            os.mkdir('./root')
            os.mkdir('./root/a')
            os.mkdir('./root/a/b')
        except FileExistsError:
            pass
        os.system('touch ./root/file_r ./root/a/file_a ./root/a/b/file_b')
    def test(self):
        self.assertEqual(recursive_file_list('./root'),
            [
                './root/file_r',
                './root/a/file_a',
                './root/a/b/file_b',
            ])
        shutil.rmtree('./root')
