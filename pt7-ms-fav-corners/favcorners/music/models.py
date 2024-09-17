from django.db import models
from django.core.files.storage import default_storage
from django.contrib.auth import get_user_model

User = get_user_model()

class MusicCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Song(models.Model):
    category = models.ForeignKey(MusicCategory, related_name='songs', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='songs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} by {self.artist}'

    def delete(self, *args, **kwargs):
        # Delete the audio file from storage when the Song is deleted
        if self.audio_file and default_storage.exists(self.audio_file.path):
            default_storage.delete(self.audio_file.path)
        
        # Call the superclass delete method to ensure the instance itself is deleted
        super().delete(*args, **kwargs)
