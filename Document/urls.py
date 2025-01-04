from django.urls import include, path
from .views import *
urlpatterns = [
    # Upload a file (image or PDF)
    path('upload/', upload_file, name='upload-file'),

]