from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from ...models import PDF
from ...serializers import PDFSerializer

class PDFListTests(TestCase):
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

    def test_pdf_list_success(self):
        """
        Test that the pdf_list endpoint returns a list of all PDFs.
        """
        # Send a GET request to the pdf_list endpoint
        response = self.client.get('/api/pdfs/')

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response data
        pdfs = PDF.objects.all()
        serializer = PDFSerializer(pdfs, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_pdf_list_empty(self):
        """
        Test that the pdf_list endpoint returns an empty list if no PDFs exist.
        """
        # Delete all PDFs
        PDF.objects.all().delete()

        # Send a GET request to the pdf_list endpoint
        response = self.client.get('/api/pdfs/')

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_pdf_list_error_handling(self):
        """
        Test that the pdf_list endpoint handles exceptions gracefully.
        """
        # Simulate an exception during database query
        original_all = PDF.objects.all
        PDF.objects.all = lambda: (_ for _ in ()).throw(Exception("Database error"))

        # Send a GET request to the pdf_list endpoint
        response = self.client.get('/api/pdfs/')

        # Restore the original all method
        PDF.objects.all = original_all

        # Verify the response status code and error message
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("An error occurred", response.data["error"])
