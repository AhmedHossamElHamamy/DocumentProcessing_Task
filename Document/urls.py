from django.urls import include, path
from .views import *

urlpatterns = [
    # Upload a file (image or PDF)
    path('upload/', upload_file, name='upload-file'),

    #file_to_base64 (image or PDF)
    path('file_to_base64/', file_to_base64, name='file_to_base64'),

    # List all images
    path('images/', image_list, name='image-list'),

    # List all PDFs
    path('pdfs/', pdf_list, name='pdf-list'),

    # Retrieve details of a specific image
    path('images/<int:id>/', image_detail, name='image-detail'),

    # Retrieve details of a specific PDF
    path('pdfs/<int:id>/', pdf_detail, name='pdf-detail'),

    # Delete a specific image
    path('images/delete/<int:id>', image_delete, name='image-delete'),

    # Delete a specific PDF
    path('pdfs/delete/<int:id>', pdf_delete, name='pdf-delete'),

    


]