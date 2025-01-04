from rest_framework import serializers
from .models import Image, PDF

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'file', 'width', 'height', 'channels', 'uploaded_at']
        read_only_fields = ['width', 'height', 'channels', 'uploaded_at']

    def to_representation(self, instance):
        """
        Customize the representation of the image file URL.
        """
        representation = super().to_representation(instance)
        representation['file'] = instance.file.url  # Return the full URL of the image file
        return representation

class PDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDF
        fields = ['id', 'file', 'num_pages', 'page_width', 'page_height', 'uploaded_at']
        read_only_fields = ['num_pages', 'page_width', 'page_height', 'uploaded_at']

    def to_representation(self, instance):
        """
        Customize the representation of the PDF file URL.
        """
        representation = super().to_representation(instance)
        representation['file'] = instance.file.url  # Return the full URL of the PDF file
        return representation