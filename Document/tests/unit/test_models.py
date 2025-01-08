from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from ...models import Image, PDF

class ImageModelTests(TestCase):
    def test_create_image(self):
        """
        Test that an Image instance can be created and saved to the database.
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

        # Verify the image was saved correctly
        self.assertTrue(image.file.name.startswith('images/test_image'))
        self.assertTrue(image.file.name.endswith('.jpg'))
        self.assertEqual(image.width, 800)
        self.assertEqual(image.height, 600)
        self.assertEqual(image.channels, 3)
        self.assertIsNotNone(image.uploaded_at)

    def test_image_str_representation(self):
        """
        Test the __str__ method of the Image model.
        """
        mock_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'simple image content',
            content_type='image/jpeg'
        )
        image = Image.objects.create(file=mock_image)
        self.assertTrue(str(image).startswith('images/test_image'))
        self.assertTrue(str(image).endswith('.jpg'))


class PDFModelTests(TestCase):
    def test_create_pdf(self):
        """
        Test that a PDF instance can be created and saved to the database.
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

        # Verify the PDF was saved correctly
        self.assertTrue(pdf.file.name.startswith('pdfs/test_pdf'))
        self.assertTrue(pdf.file.name.endswith('.pdf'))
        self.assertEqual(pdf.num_pages, 10)
        self.assertEqual(pdf.page_width, 595.0)
        self.assertEqual(pdf.page_height, 842.0)
        self.assertIsNotNone(pdf.uploaded_at)

    def test_pdf_str_representation(self):
        """
        Test the __str__ method of the PDF model.
        """
        mock_pdf = SimpleUploadedFile(
            name='test_pdf.pdf',
            content=b'simple pdf content',
            content_type='application/pdf'
        )
        pdf = PDF.objects.create(file=mock_pdf)
        self.assertTrue(str(pdf).startswith('pdfs/test_pdf'))
        self.assertTrue(str(pdf).endswith('.pdf'))