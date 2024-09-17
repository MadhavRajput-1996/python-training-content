from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.files.storage import default_storage

class CustomUser(AbstractUser):
    PROFESSION_CHOICES = [
        ('student', 'Student'),
        ('business', 'Business'),
        ('entrepreneur', 'Entrepreneur'),
        ('other', 'Other'),
    ]
    
    email = models.EmailField(unique=True)
    profession = models.CharField(max_length=20, choices=PROFESSION_CHOICES)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Only delete the old profile picture if a new one is being uploaded
        try:
            this = CustomUser.objects.get(id=self.id)
            if this.profile_pic != self.profile_pic and this.profile_pic.name != 'default.jpg':
                # Delete the old profile picture if it's not the default picture
                if default_storage.exists(this.profile_pic.path):
                    default_storage.delete(this.profile_pic.path)
        except CustomUser.DoesNotExist:
            pass  # No need to delete anything if it's a new user

        super().save(*args, **kwargs)
