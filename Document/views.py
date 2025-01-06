import io
import os
from django.http import Http404
from django.shortcuts import get_object_or_404, render
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
import fitz  # PyMuPDF


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

#Extra API to get file in base64
@api_view(['POST'])
def file_to_base64(request):
    # Get the file path from the request data
    file_path = request.data.get('file_path')

    # Validate the file path
    if not file_path:
        return Response({"error": "File path is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Convert to absolute path
    absolute_path = os.path.abspath(file_path)

    # Security: Prevent directory traversal attacks
    if ".." in absolute_path or not os.path.exists(absolute_path):
        return Response({"error": "Invalid file path"}, status=status.HTTP_400_BAD_REQUEST)

    # Get file extension
    _, file_extension = os.path.splitext(absolute_path)
    file_extension = file_extension.lower()

    # List of image extensions
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
    # List of PDF extensions
    pdf_extensions = ['.pdf']

    if file_extension in image_extensions:
        try:
            # Open the image file using the alias
            with PILImage.open(absolute_path) as img:
                # Get image properties
                width, height = img.size
                # Read the image content and encode to base64
                with open(absolute_path, "rb") as file:
                    base64_data = base64.b64encode(file.read()).decode("utf-8")
                # Return base64 data and image properties
                return Response({
                    "base64": base64_data
                }, status=status.HTTP_200_OK)
        except PermissionError:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif file_extension in pdf_extensions:
        try:
            # Read the PDF file and encode to base64
            with open(absolute_path, "rb") as file:
                base64_data = base64.b64encode(file.read()).decode("utf-8")
            # Return base64 data
            return Response({
                "base64": base64_data
            }, status=status.HTTP_200_OK)
        except PermissionError:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"error": "Unsupported file type"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def image_list(request):
    try:
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def pdf_list(request):
    try:
        pdfs = PDF.objects.all()
        serializer = PDFSerializer(pdfs, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def image_detail(request, id):
    try:
        # Attempt to fetch the image by ID
        image = get_object_or_404(Image, id=id)
        serializer = ImageSerializer(image)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Http404:
        # Handle the case where the image is not found
        return Response({"error": "Image not found."}, status=status.HTTP_404_NOT_FOUND)
    except ValueError as ve:
        # Handle value-related errors (e.g., invalid ID format)
        return Response({"error": f"Invalid ID: {str(ve)}"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # Catch any other unexpected errors
        return Response({"error": f"An internal error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def pdf_detail(request, id):
    try:
        # Attempt to fetch the PDF by ID
        pdf = get_object_or_404(PDF, id=id)
        serializer = PDFSerializer(pdf)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Http404:
        # Handle the case where the PDF is not found
        return Response({"error": "PDF not found."}, status=status.HTTP_404_NOT_FOUND)
    except ValueError as ve:
        # Handle value-related errors (e.g., invalid ID format)
        return Response({"error": f"Invalid ID: {str(ve)}"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # Catch any other unexpected errors
        return Response({"error": f"An internal error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def image_delete(request, id):
    try:
        image = get_object_or_404(Image, id=id)
        image.file.delete()  # Delete the file from the filesystem
        image.delete()  # Delete the record from the database
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def pdf_delete(request, id):
    try:
        pdf = get_object_or_404(PDF, id=id)
        pdf.file.delete()  # Delete the file from the filesystem
        pdf.delete()  # Delete the record from the database
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def rotate_image(request):
    image_id = request.data.get('image_id')
    angle = request.data.get('angle')

    # Validate required fields
    if not image_id:
        return Response({"error": "Image ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    if not angle:
        return Response({"error": "Rotation angle is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        image = Image.objects.get(id=image_id)
        pil_image = PILImage.open(image.file)
        rotated_image = pil_image.rotate(int(angle))
        buffer = io.BytesIO()
        rotated_image.save(buffer, format='PNG')
        image.file.save(f'rotated_{image.file.name}', ContentFile(buffer.getvalue()))
        image.save()

        serializer = ImageSerializer(image)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Image.DoesNotExist:
        return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def convert_pdf_to_image(request):
    pdf_id = request.data.get('pdf_id')
    if not pdf_id:
        return Response({"error": "PDF ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Get the PDF object
        pdf = PDF.objects.get(id=pdf_id)
        pdf.file.seek(0)
        pdf_content = pdf.file.read()

        # Open the PDF using PyMuPDF
        pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
        image_list = []

        # Convert each page to an image
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            pix = page.get_pixmap()
            img_data = pix.tobytes()

            # Create a PIL Image object from the image data
            pil_image = PILImage.open(io.BytesIO(img_data))

            # Extract image metadata
            width, height = pil_image.size
            channels = len(pil_image.getbands())

            # Save the image to a ContentFile
            buffer = io.BytesIO()
            pil_image.save(buffer, format="PNG")
            image_file = ContentFile(buffer.getvalue(), name=f'page_{page_num+1}.png')

            # Save the image to the database
            new_image = Image(file=image_file, width=width, height=height, channels=channels)
            new_image.save()

            # Serialize the image and add it to the response list
            image_list.append(ImageSerializer(new_image).data)

        return Response(image_list, status=status.HTTP_200_OK)

    except PDF.DoesNotExist:
        return Response({"error": "PDF not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)