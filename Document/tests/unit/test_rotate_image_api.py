from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from io import BytesIO
from PIL import Image as PILImage
from django.core.files.uploadedfile import SimpleUploadedFile
from ...models import Image  # Adjust the import based on your project structure
from ...serializers import ImageSerializer  # Adjust the import based on your project structure

class RotateImageTests(TestCase):
    def setUp(self):
        """
        Set up the test client and create a test image.
        """
        self.client = APIClient()

        # Create an actual image file
        image_file = BytesIO()
        PILImage.new('RGB', (100, 100)).save(image_file, 'PNG')
        image_file.seek(0)

        # Create a test image with the actual image file
        self.image = Image.objects.create(
            file=SimpleUploadedFile('test_image.png', image_file.read(), content_type='image/png'),
            width=100,
            height=100,
            channels=3
        )

    def test_rotate_image_success(self):
        """
        Test that the rotate_image endpoint rotates an image successfully.
        """
        # Data for the request
        data = {
            'image_id': self.image.id,
            'angle': 90
        }

        # Send a POST request to the rotate_image endpoint
        response = self.client.post('/api/rotate/', data, format='json')

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the image was updated in the database
        updated_image = Image.objects.get(id=self.image.id)

        # Verify the response data matches the updated image
        serializer = ImageSerializer(updated_image)
        self.assertEqual(response.data, serializer.data)

    def test_rotate_image_missing_image_id(self):
        """
        Test that the rotate_image endpoint returns a 400 error if image_id is missing.
        """
        # Data for the request (missing image_id)
        data = {
            'angle': 90
        }

        # Send a POST request to the rotate_image endpoint
        response = self.client.post('/api/rotate/', data, format='json')

        # Verify the response status code and error message
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Image ID is required"})

    def test_rotate_image_missing_angle(self):
        """
        Test that the rotate_image endpoint returns a 400 error if angle is missing.
        """
        # Data for the request (missing angle)
        data = {
            'image_id': self.image.id
        }

        # Send a POST request to the rotate_image endpoint
        response = self.client.post('/api/rotate/', data, format='json')

        # Verify the response status code and error message
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Rotation angle is required"})

    def test_rotate_image_invalid_image_id(self):
        """
        Test that the rotate_image endpoint returns a 404 error if the image does not exist.
        """
        # Data for the request (invalid image_id)
        data = {
            'image_id': 999,  # Non-existent ID
            'angle': 90
        }

        # Send a POST request to the rotate_image endpoint
        response = self.client.post('/api/rotate/', data, format='json')

        # Verify the response status code and error message
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Image not found"})

    @patch('PIL.Image.open')
    def test_rotate_image_error_handling(self, mock_image_open):
        """
        Test that the rotate_image endpoint handles unexpected errors gracefully.
        """
        # Mock PIL.Image.open to raise an exception
        mock_image_open.side_effect = Exception("Image processing error")

        # Data for the request
        data = {
            'image_id': self.image.id,
            'angle': 90
        }

        # Send a POST request to the rotate_image endpoint
        response = self.client.post('/api/rotate/', data, format='json')

        # Verify the response status code and error message
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data, {"error": "An error occurred: Image processing error"})