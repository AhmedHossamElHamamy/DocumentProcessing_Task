from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.shortcuts import get_object_or_404
from ...models import Image

class ImageDeleteTests(TestCase):
    def setUp(self):
        """
        Set up the test client and create a test image.
        """
        self.client = APIClient()

        # Create a test image
        self.image = Image.objects.create(
            file='images/test_image.png',
            width=800,
            height=600,
            channels=3
        )

    def test_image_delete_success(self):
        """
        Test that the image_delete endpoint deletes the image successfully.
        """
        print("Image ID:", self.image.id)
        print("Request URL:", f'/api/images/delete/{self.image.id}')

        # Debug: Verify that the image exists in the database
        image_exists = Image.objects.filter(id=self.image.id).exists()
        print("Image exists in database:", image_exists)

        # Send a DELETE request to the image_delete endpoint
        response = self.client.delete(f'/api/images/delete/{self.image.id}')

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



    def test_image_delete_not_found(self):
        """
        Test that the image_delete endpoint returns a 404 if the image does not exist.
        """
        # Send a DELETE request with a non-existent ID
        response = self.client.delete('api/images/delete/999')

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('Document.views.get_object_or_404')
    def test_image_delete_error_handling(self, mock_get_object_or_404):
        """
        Test that the image_delete endpoint handles exceptions gracefully.
        """
        # Mock get_object_or_404 to raise an exception
        mock_get_object_or_404.side_effect = Exception("Database error")

        # Send a DELETE request to the image_delete endpoint
        response = self.client.delete(f'/api/images/delete/{self.image.id}')

        # Verify the response status code and error message
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data, {"error": "An error occurred: Database error"})