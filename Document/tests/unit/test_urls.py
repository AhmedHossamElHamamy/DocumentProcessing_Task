from django.test import TestCase
from django.urls import reverse, resolve

class URLTests(TestCase):
    def test_upload_file_url(self):
        """
        Test that the 'upload-file' URL resolves to the correct view.
        """
        url = reverse('upload-file')
        self.assertEqual(resolve(url).view_name, 'upload-file')

    def test_file_to_base64_url(self):
        """
        Test that the 'file_to_base64' URL resolves to the correct view.
        """
        url = reverse('file_to_base64')
        self.assertEqual(resolve(url).view_name, 'file_to_base64')

    def test_image_list_url(self):
        """
        Test that the 'image-list' URL resolves to the correct view.
        """
        url = reverse('image-list')
        self.assertEqual(resolve(url).view_name, 'image-list')

    def test_pdf_list_url(self):
        """
        Test that the 'pdf-list' URL resolves to the correct view.
        """
        url = reverse('pdf-list')
        self.assertEqual(resolve(url).view_name, 'pdf-list')

    def test_image_detail_url(self):
        """
        Test that the 'image-detail' URL resolves to the correct view.
        """
        url = reverse('image-detail', args=[1])  # Use a sample ID
        self.assertEqual(resolve(url).view_name, 'image-detail')

    def test_pdf_detail_url(self):
        """
        Test that the 'pdf-detail' URL resolves to the correct view.
        """
        url = reverse('pdf-detail', args=[1])  # Use a sample ID
        self.assertEqual(resolve(url).view_name, 'pdf-detail')

    def test_image_delete_url(self):
        """
        Test that the 'image-delete' URL resolves to the correct view.
        """
        url = reverse('image-delete', args=[1])  # Use a sample ID
        self.assertEqual(resolve(url).view_name, 'image-delete')

    def test_pdf_delete_url(self):
        """
        Test that the 'pdf-delete' URL resolves to the correct view.
        """
        url = reverse('pdf-delete', args=[1])  # Use a sample ID
        self.assertEqual(resolve(url).view_name, 'pdf-delete')

    def test_rotate_image_url(self):
        """
        Test that the 'rotate-image' URL resolves to the correct view.
        """
        url = reverse('rotate-image')
        self.assertEqual(resolve(url).view_name, 'rotate-image')

    def test_convert_pdf_to_image_url(self):
        """
        Test that the 'convert-pdf-to-image' URL resolves to the correct view.
        """
        url = reverse('convert-pdf-to-image')
        self.assertEqual(resolve(url).view_name, 'convert-pdf-to-image')