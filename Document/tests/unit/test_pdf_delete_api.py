from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.shortcuts import get_object_or_404
from ...models import PDF  # Adjust the import based on your project structure

class PDFDeleteTests(TestCase):
    def setUp(self):
        """
        Set up the test client and create some test PDFs.
        """
        self.client = APIClient()

        # Create test PDFs
        self.pdf1 = PDF.objects.create(
            file='pdfs/test_pdf1.pdf',
            num_pages=10,
            page_width=8.5,
            page_height=11.0
        )
    def test_pdf_delete_success(self):
        """
        Test that the pdf_delete endpoint deletes the PDF successfully.
        """
        print("PDF ID:", self.pdf1.id)
        print("Request URL:", f'/api/pdfs/delete/{self.pdf1.id}')

        # Debug: Verify that the PDF exists in the database
        pdf_exists = PDF.objects.filter(id=self.pdf1.id).exists()
        print("PDF exists in database:", pdf_exists)

        # Send a DELETE request to the pdf_delete endpoint
        response = self.client.delete(f'/api/pdfs/delete/{self.pdf1.id}')

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify the PDF was deleted from the database
        with self.assertRaises(PDF.DoesNotExist):
            PDF.objects.get(id=self.pdf1.id)

    def test_pdf_delete_not_found(self):
        """
        Test that the pdf_delete endpoint returns a 404 if the PDF does not exist.
        """
        # Send a DELETE request with a non-existent ID
        response = self.client.delete('api/pdfs/delete/999')

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('Document.views.get_object_or_404')
    def test_pdf_delete_error_handling(self, mock_get_object_or_404):
        """
        Test that the pdf_delete endpoint handles exceptions gracefully.
        """
        # Mock get_object_or_404 to raise an exception
        mock_get_object_or_404.side_effect = Exception("Database error")

        # Send a DELETE request to the pdf_delete endpoint
        response = self.client.delete(f'/api/pdfs/delete/{self.pdf1.id}')

        # Verify the response status code and error message
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data, {"error": "An error occurred: Database error"})