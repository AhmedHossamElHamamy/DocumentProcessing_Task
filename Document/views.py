from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Image, PDF
from .serializers import ImageSerializer, PDFSerializer
import base64
from django.core.files.base import ContentFile
from PIL import Image as PILImage, UnidentifiedImageError
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError
import uuid  # For generating unique filenames

# Create your views here.
@api_view(['POST'])
def upload_file(request):
    file_data = request.data.get('file')
    file_type = request.data.get('type')  # 'image' or 'pdf'

    # Validate required fields
    if not file_data:
        return Response({"error": "File data is required"}, status=status.HTTP_400_BAD_REQUEST)
    if not file_type:
        return Response({"error": "File type is required (image or pdf)"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Decode base64 file data
        decoded_file = base64.b64decode(file_data)

        # Generate a unique filename with the correct extension
        if file_type == 'image':
            file_extension = '.png'  # Default extension for images
        elif file_type == 'pdf':
            file_extension = '.pdf'  # Default extension for PDFs
        else:
            return Response({"error": "Invalid file type. Supported types: image, pdf"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a unique filename
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_content = ContentFile(decoded_file, name=unique_filename)

        if file_type == 'image':
            try:
                # Validate and process the image
                pil_image = PILImage.open(file_content)
                width, height = pil_image.size
                channels = len(pil_image.getbands())

                image = Image(file=file_content, width=width, height=height, channels=channels)
                image.save()

                serializer = ImageSerializer(image)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            except UnidentifiedImageError:
                return Response({"error": "Invalid image file"}, status=status.HTTP_400_BAD_REQUEST)

        elif file_type == 'pdf':
            try:
                # Validate and process the PDF
                pdf_reader = PdfReader(file_content)
                num_pages = len(pdf_reader.pages)
                page_width = pdf_reader.pages[0].mediabox.width
                page_height = pdf_reader.pages[0].mediabox.height

                pdf = PDF(file=file_content, num_pages=num_pages, page_width=page_width, page_height=page_height)
                pdf.save()

                serializer = PDFSerializer(pdf)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            except PdfReadError:
                return Response({"error": "Invalid PDF file"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
