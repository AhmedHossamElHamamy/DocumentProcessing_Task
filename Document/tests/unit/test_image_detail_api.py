from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.shortcuts import get_object_or_404
from ...models import Image
from ...serializers import ImageSerializer

class ImageDetailTests(TestCase):
    def setUp(self):
        """
        Set up the test client and create some test images.
        """
        self.client = APIClient()

        # Create test images
        self.image1 = Image.objects.create(
            file='images/test_image1.png',
            width=800,
            height=600,
            channels=3
        )
        self.image2 = Image.objects.create(
            file='images/test_image2.png',
            width=1024,
            height=768,
            channels=3
        )

    def test_image_detail_success(self):
        """
        Test that the image_detail endpoint returns the correct image details.
        """
        # Send a GET request to the image_detail endpoint for image1
        response = self.client.get(f'/api/images/{self.image1.id}/')

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response data
        image = get_object_or_404(Image, id=self.image1.id)
        serializer = ImageSerializer(image)
        self.assertEqual(response.data, serializer.data)

    def test_image_detail_not_found(self):
        """
        Test that the image_detail endpoint returns a 404 if the image does not exist.
        """
        # Send a GET request to the image_detail endpoint with a non-existent ID
        response = self.client.get('/api/images/999/')

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    @patch('Document.views.get_object_or_404')
    def test_image_detail_error_handling(self, mock_get_object_or_404):
        """
        Test that the image_detail endpoint handles exceptions gracefully.
        """
        # Mock get_object_or_404 to raise an exception
        mock_get_object_or_404.side_effect = Exception("Database error")

        # Send a GET request to the image_detail endpoint
        response = self.client.get(f'/api/images/{self.image1.id}/')

        # Verify the response status code and error message
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("An internal error occurred", response.data["error"])