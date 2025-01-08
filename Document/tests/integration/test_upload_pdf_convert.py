from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
import base64
from PyPDF2 import PdfReader
from ...models import PDF, Image  # Adjust the import based on your project structure
from ...serializers import ImageSerializer  # Adjust the import based on your project structure


class UploadAndConvertPDFIntegrationTest(TestCase):
    def setUp(self):
        """
        Set up the test client.
        """
        self.client = APIClient()

    def test_upload_and_convert_pdf(self):
        """
        Test the workflow: upload a PDF and convert it to images.
        """
        # Step 1: Upload a PDF
        # Create a valid mock PDF file
        pdf_content = b"%PDF-1.4\n1 0 obj\n<</Type/Catalog/Pages 2 0 R>>\nendobj\n2 0 obj\n<</Type/Pages/Kids[3 0 R]/Count 1>>\nendobj\n3 0 obj\n<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]>>\nendobj\nxref\n0 4\n0000000000 65535 f\n0000000010 00000 n\n0000000053 00000 n\n0000000102 00000 n\ntrailer\n<</Size 4/Root 1 0 R>>\nstartxref\n149\n%%EOF"
        base64_pdf = base64.b64encode(pdf_content).decode('utf-8')

        # Send a POST request to upload the PDF
        upload_response = self.client.post(
            '/api/upload/',
            {'file': base64_pdf, 'type': 'pdf'},
            format='json'
        )

        # Verify the upload response
        self.assertEqual(upload_response.status_code, status.HTTP_201_CREATED)
        self.assertIn('file', upload_response.data)
        self.assertTrue(upload_response.data['file'].startswith('/media/pdfs/'))
        self.assertTrue(upload_response.data['file'].endswith('.pdf'))

        # Verify PDF metadata
        pdf_reader = PdfReader(BytesIO(pdf_content))
        self.assertEqual(upload_response.data['num_pages'], len(pdf_reader.pages))  # Number of pages in the mock PDF
        self.assertEqual(upload_response.data['page_width'], pdf_reader.pages[0].mediabox.width)  # Page width of the mock PDF
        self.assertEqual(upload_response.data['page_height'], pdf_reader.pages[0].mediabox.height)  # Page height of the mock PDF

        # Get the uploaded PDF ID
        pdf_id = upload_response.data['id']

        # Step 2: Convert the uploaded PDF to images
        # Data for the convert_pdf_to_image request
        convert_data = {
            'pdf_id': pdf_id
        }

        # Send a POST request to the convert_pdf_to_image endpoint
        convert_response = self.client.post('/api/convert_pdf_to_image/', convert_data, format='json')

        # Verify the convert response status code
        self.assertEqual(convert_response.status_code, status.HTTP_200_OK)

        # Step 3: Verify the converted images
        # Verify the response data contains the converted images
        self.assertIsInstance(convert_response.data, list)
        self.assertEqual(len(convert_response.data), upload_response.data['num_pages'])

        # Verify the images were saved to the database
        images = Image.objects.all()
        self.assertEqual(images.count(), upload_response.data['num_pages'])

        # Verify the response data matches the serialized images
        serializer = ImageSerializer(images, many=True)
        self.assertEqual(convert_response.data, serializer.data)