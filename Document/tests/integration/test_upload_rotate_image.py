from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image as PILImage
import base64
from ...models import Image  # Adjust the import based on your project structure
from ...serializers import ImageSerializer  # Adjust the import based on your project structure


class UploadAndRotateImageIntegrationTest(TestCase):
    def setUp(self):
        """
        Set up the test client.
        """
        self.client = APIClient()

    def test_upload_and_rotate_image(self):
        """
        Test the workflow: upload an image and rotate it.
        """
        # Step 1: Upload an image
        # Create a valid mock image file (PNG format)
        image_file = BytesIO()
        PILImage.new('RGB', (100, 100)).save(image_file, 'PNG')
        image_file.seek(0)
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        # Send a POST request to upload the image
        upload_response = self.client.post(
            '/api/upload/',
            {'file': base64_image, 'type': 'image'},
            format='json'
        )

        # Verify the upload response
        self.assertEqual(upload_response.status_code, status.HTTP_201_CREATED)
        self.assertIn('file', upload_response.data)
        self.assertTrue(upload_response.data['file'].startswith('/media/images/'))
        self.assertTrue(upload_response.data['file'].endswith('.png'))

        # Verify image metadata
        pil_image = PILImage.open(image_file)
        self.assertEqual(upload_response.data['width'], pil_image.size[0])  # Width of the mock image
        self.assertEqual(upload_response.data['height'], pil_image.size[1])  # Height of the mock image
        self.assertEqual(upload_response.data['channels'], len(pil_image.getbands()))  # Channels of the mock image

        # Get the uploaded image ID
        image_id = upload_response.data['id']

        # Step 2: Rotate the uploaded image
        # Data for the rotate_image request
        rotate_data = {
            'image_id': image_id,
            'angle': 90
        }

        # Send a POST request to the rotate_image endpoint
        rotate_response = self.client.post('/api/rotate/', rotate_data, format='json')

        # Verify the rotate response status code
        self.assertEqual(rotate_response.status_code, status.HTTP_200_OK)

        # Step 3: Verify the rotated image
        # Retrieve the updated image from the database
        updated_image = Image.objects.get(id=image_id)

        # Verify the response data matches the updated image
        serializer = ImageSerializer(updated_image)
        self.assertEqual(rotate_response.data, serializer.data)

        # Verify the image metadata after rotation
        rotated_pil_image = PILImage.open(updated_image.file)
        self.assertEqual(rotate_response.data['width'], rotated_pil_image.size[0])  # Width after rotation
        self.assertEqual(rotate_response.data['height'], rotated_pil_image.size[1])  # Height after rotation
        self.assertEqual(rotate_response.data['channels'], len(rotated_pil_image.getbands()))  # Channels after rotation