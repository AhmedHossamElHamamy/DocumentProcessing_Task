from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from ...models import PDF, Image  # Adjust the import based on your project structure
from ...serializers import ImageSerializer  # Adjust the import based on your project structure

class ConvertPDFToImageTests(TestCase):
    def setUp(self):
        """
        Set up the test client and create a test PDF.
        """
        self.client = APIClient()

        # Create a test PDF file
        pdf_content = b"%PDF-1.4\n1 0 obj\n<</Type/Catalog/Pages 2 0 R>>\nendobj\n2 0 obj\n<</Type/Pages/Kids[3 0 R]/Count 1>>\nendobj\n3 0 obj\n<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]>>\nendobj\nxref\n0 4\n0000000000 65535 f\n0000000010 00000 n\n0000000053 00000 n\n0000000102 00000 n\ntrailer\n<</Size 4/Root 1 0 R>>\nstartxref\n149\n%%EOF"
        self.pdf = PDF.objects.create(
            file=SimpleUploadedFile('test.pdf', pdf_content, content_type='application/pdf'),
            num_pages=1,
            page_width=612,
            page_height=792
        )

    def test_convert_pdf_to_image_success(self):
        """
        Test that the convert_pdf_to_image endpoint converts a PDF to images successfully.
        """
        # Data for the request
        data = {
            'pdf_id': self.pdf.id
        }

        # Send a POST request to the convert_pdf_to_image endpoint
        response = self.client.post('/api/convert_pdf_to_image/', data, format='json')

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response data contains the converted images
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), self.pdf.num_pages)

        # Verify the images were saved to the database
        images = Image.objects.all()
        self.assertEqual(images.count(), self.pdf.num_pages)

        # Verify the response data matches the serialized images
        serializer = ImageSerializer(images, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_convert_pdf_to_image_missing_pdf_id(self):
        """
        Test that the convert_pdf_to_image endpoint returns a 400 error if pdf_id is missing.
        """
        # Data for the request (missing pdf_id)
        data = {}

        # Send a POST request to the convert_pdf_to_image endpoint
        response = self.client.post('/api/convert_pdf_to_image/', data, format='json')

        # Verify the response status code and error message
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "PDF ID is required"})

    def test_convert_pdf_to_image_invalid_pdf_id(self):
        """
        Test that the convert_pdf_to_image endpoint returns a 404 error if the PDF does not exist.
        """
        # Data for the request (invalid pdf_id)
        data = {
            'pdf_id': 999  # Non-existent ID
        }

        # Send a POST request to the convert_pdf_to_image endpoint
        response = self.client.post('/api/convert_pdf_to_image/', data, format='json')

        # Verify the response status code and error message
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "PDF not found"})

    @patch('fitz.open')
    def test_convert_pdf_to_image_error_handling(self, mock_fitz_open):
        """
        Test that the convert_pdf_to_image endpoint handles unexpected errors gracefully.
        """
        # Mock fitz.open to raise an exception
        mock_fitz_open.side_effect = Exception("PDF processing error")

        # Data for the request
        data = {
            'pdf_id': self.pdf.id
        }

        # Send a POST request to the convert_pdf_to_image endpoint
        response = self.client.post('/api/convert_pdf_to_image/', data, format='json')

        # Verify the response status code and error message
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data, {"error": "An error occurred: PDF processing error"})