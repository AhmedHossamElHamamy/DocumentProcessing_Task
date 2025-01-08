from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.exceptions import ValidationError
from ...models import Image, PDF
from ...serializers import ImageSerializer, PDFSerializer

@override_settings(MEDIA_URL='/media/')
class ImageSerializerTests(TestCase):
    def test_image_serializer_valid_data(self):
        """
        Test that the ImageSerializer correctly serializes valid data.
        """
        # Create a mock image file
        mock_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'simple image content',
            content_type='image/jpeg'
        )

        # Create an Image instance
        image = Image.objects.create(
            file=mock_image,
            width=800,
            height=600,
            channels=3
        )

        # Serialize the image instance
        serializer = ImageSerializer(image)

        # Verify the serialized data
        self.assertEqual(serializer.data['id'], image.id)
        self.assertTrue(serializer.data['file'].startswith('/media/images/test_image'))
        self.assertTrue(serializer.data['file'].endswith('.jpg'))
        self.assertEqual(serializer.data['width'], 800)
        self.assertEqual(serializer.data['height'], 600)
        self.assertEqual(serializer.data['channels'], 3)
        self.assertIsNotNone(serializer.data['uploaded_at'])

    def test_image_serializer_invalid_data(self):
        """
        Test that the ImageSerializer raises validation errors for invalid data.
        """
        # Invalid data (missing required 'file' field)
        invalid_data = {
            'width': 800,
            'height': 600,
            'channels': 3
        }

        serializer = ImageSerializer(data=invalid_data)

        # Verify that the serializer raises a validation error
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_image_serializer_to_representation(self):
        """
        Test the custom to_representation method of the ImageSerializer.
        """
        # Create a mock image file
        mock_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'simple image content',
            content_type='image/jpeg'
        )

        # Create an Image instance
        image = Image.objects.create(
            file=mock_image,
            width=800,
            height=600,
            channels=3
        )

        # Serialize the image instance
        serializer = ImageSerializer(image)

        # Verify that the 'file' field contains the full URL
        self.assertTrue(serializer.data['file'].startswith('/media/images/test_image'))
        self.assertTrue(serializer.data['file'].endswith('.jpg'))


@override_settings(MEDIA_URL='/media/')
class PDFSerializerTests(TestCase):
    def test_pdf_serializer_valid_data(self):
        """
        Test that the PDFSerializer correctly serializes valid data.
        """
        # Create a mock PDF file
        mock_pdf = SimpleUploadedFile(
            name='test_pdf.pdf',
            content=b'simple pdf content',
            content_type='application/pdf'
        )

        # Create a PDF instance
        pdf = PDF.objects.create(
            file=mock_pdf,
            num_pages=10,
            page_width=595.0,
            page_height=842.0
        )

        # Serialize the PDF instance
        serializer = PDFSerializer(pdf)

        # Verify the serialized data
        self.assertEqual(serializer.data['id'], pdf.id)
        self.assertTrue(serializer.data['file'].startswith('/media/pdfs/test_pdf'))
        self.assertTrue(serializer.data['file'].endswith('.pdf'))
        self.assertEqual(serializer.data['num_pages'], 10)
        self.assertEqual(serializer.data['page_width'], 595.0)
        self.assertEqual(serializer.data['page_height'], 842.0)
        self.assertIsNotNone(serializer.data['uploaded_at'])

    def test_pdf_serializer_invalid_data(self):
        """
        Test that the PDFSerializer raises validation errors for invalid data.
        """
        # Invalid data (missing required 'file' field)
        invalid_data = {
            'num_pages': 10,
            'page_width': 595.0,
            'page_height': 842.0
        }

        serializer = PDFSerializer(data=invalid_data)

        # Verify that the serializer raises a validation error
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_pdf_serializer_to_representation(self):
        """
        Test the custom to_representation method of the PDFSerializer.
        """
        # Create a mock PDF file
        mock_pdf = SimpleUploadedFile(
            name='test_pdf.pdf',
            content=b'simple pdf content',
            content_type='application/pdf'
        )

        # Create a PDF instance
        pdf = PDF.objects.create(
            file=mock_pdf,
            num_pages=10,
            page_width=595.0,
            page_height=842.0
        )

        # Serialize the PDF instance
        serializer = PDFSerializer(pdf)

        # Verify that the 'file' field contains the full URL
        self.assertTrue(serializer.data['file'].startswith('/media/pdfs/test_pdf'))
        self.assertTrue(serializer.data['file'].endswith('.pdf'))