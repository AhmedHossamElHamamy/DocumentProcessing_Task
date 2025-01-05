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


]