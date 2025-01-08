from unittest.mock import patch
from django.shortcuts import get_object_or_404
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from Document.serializers import PDFSerializer
from ...models import PDF

class PDFDetailTests(TestCase):
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
        self.pdf2 = PDF.objects.create(
            file='pdfs/test_pdf2.pdf',
            num_pages=15,
            page_width=8.5,
            page_height=14.0
        )

    def test_pdf_detail_success(self):
        """
        Test that the pdf_detail endpoint returns the correct PDF details.
        """
        # Send a GET request to the pdf_detail endpoint for pdf1
        response = self.client.get(f'/api/pdfs/{self.pdf1.id}/')

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response data
        pdf=get_object_or_404(PDF, id=self.pdf1.id)
        serializer = PDFSerializer(pdf)
        self.assertEqual(response.data, serializer.data)

    def test_pdf_detail_not_found(self):
        """
        Test that the pdf_detail endpoint returns a 404 if the PDF does not exist.
        """
        # Send a GET request to the pdf_detail endpoint with a non-existent ID
        response = self.client.get('/api/pdfs/999/')

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Verify the error message
        self.assertEqual(response.data, {"error": "PDF not found."})

    @patch('Document.views.get_object_or_404')  # Replace `app_name` with your actual app name
    def test_pdf_detail_error_handling(self, mock_get_object_or_404):
        """
        Test that the pdf_detail endpoint handles exceptions gracefully.
        """
        # Mock get_object_or_404 to raise an exception
        mock_get_object_or_404.side_effect = Exception("Database error")

        # Send a GET request to the pdf_detail endpoint
        response = self.client.get(f'/api/pdfs/{self.pdf1.id}/')

        # Verify the response status code and error message
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("An internal error occurred", response.data["error"])
