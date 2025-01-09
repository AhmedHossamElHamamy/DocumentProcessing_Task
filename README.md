# DocumentProcessing_Task

This project is a Django-based REST API for processing images and PDF files. Users can upload images and PDFs, retrieve details about uploaded files, rotate images, convert PDFs to images, and delete files. The API is built using Django Rest Framework (DRF) and is dockerized for easy deployment.

## Features
- **files to base64**: Users can upload images and PDFs and get base64 format.
- **Upload Files**: Users can upload images and PDFs in base64 format.
- **List Files**: Users can retrieve a list of all uploaded images or PDFs.
- **File Details**: Users can get details about a specific image or PDF, such as dimensions, number of pages, etc.
- **Delete Files**: Users can delete specific images or PDFs.
- **Rotate Images**: Users can rotate an image by a specified angle.
- **Convert PDF to Image**: Users can convert a PDF file to an image.
- **Dockerized**: The project is dockerized for easy deployment and testing.

## API Endpoints

### Images
- **POST /api/file_to_base64/**: Upload an image and get it at base64 format.
- **POST /api/upload/**: Upload an image or PDF in base64 format.
- **GET /api/images/**: Get a list of all uploaded images.
- **GET /api/images/{id}/**: Get details of a specific image (e.g., location, width, height, number of channels).
- **DELETE /api/images/{id}/**: Delete a specific image.
- **POST /api/rotate/**: Rotate an image by a specified angle.

### PDFs
- **POST /api/file_to_base64/**: Upload an PDF and get it at base64 format.
- **POST /api/upload/**: Upload an image or PDF in base64 format.
- **GET /api/pdfs/**: Get a list of all uploaded PDFs.
- **GET /api/pdfs/{id}/**: Get details of a specific PDF (e.g., location, number of pages, page width, page height).
- **DELETE /api/pdfs/{id}/**: Delete a specific PDF.
- **POST /api/convert-pdf-to-image/**: Convert a PDF to an image.

## Docker image link:
    https://hub.docker.com/repository/docker/ahmedelhamamy1/document_processing_task/general
## Website link on pythonanywhere:
    https://ahmedelhamamy.pythonanywhere.com/
## Postman collection link:
    https://www.postman.com/winter-resonance-717859/document-processing-task/collection/e0y635h/document-processing-task    
