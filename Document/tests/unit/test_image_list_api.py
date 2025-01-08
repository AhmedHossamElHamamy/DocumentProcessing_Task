from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from ...models import Image
from ...serializers import ImageSerializer

class ImageListTests(TestCase):
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

    def test_image_list_success(self):
        """
        Test that the image_list endpoint returns a list of all images.
        """
        # Send a GET request to the image_list endpoint
        response = self.client.get('/api/images/')

        # Verify the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response data
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_image_list_empty(self):
        """
        Test that the image_list endpoint returns an empty list if no images exist.
        """
        # Delete all images
        Image.objects.all().delete()

        # Send a GET request to the image_list endpoint
        response = self.client.get('/api/images/')

        # Verify the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_image_list_error_handling(self):
        """
        Test that the image_list endpoint handles exceptions gracefully.
        """
        # Simulate an exception during database query
        original_all = Image.objects.all
        Image.objects.all = lambda: (_ for _ in ()).throw(Exception("Database error"))

        # Send a GET request to the image_list endpoint
        response = self.client.get('/api/images/')

        # Restore the original all method
        Image.objects.all = original_all

        # Verify the response status code and error message
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("An error occurred", response.data["error"])
  