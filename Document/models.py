from django.db import models

class Image(models.Model):
    file = models.ImageField(upload_to='images/')  # Saves to 'media/images/'
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    channels = models.IntegerField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

class PDF(models.Model):
    file = models.FileField(upload_to='pdfs/')  # Saves to 'media/pdfs/'
    num_pages = models.IntegerField(blank=True, null=True)
    page_width = models.FloatField(blank=True, null=True)
    page_height = models.FloatField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name