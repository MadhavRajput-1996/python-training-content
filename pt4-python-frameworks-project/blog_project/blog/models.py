import os
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

class CustomUser(AbstractUser):
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    username = None
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1, choices=gender_choices)
    dob = models.DateField()
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

def image_upload_path(instance, filename):
    # Generate a unique filename for the image
    ext = filename.split('.')[-1]
    filename = f'{uuid4().hex}.{ext}'  # Using UUID for uniqueness
    return os.path.join('post_images', filename)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload_path, null=True, blank=True)

    def delete(self, *args, **kwargs):
        # Delete the associated image file from the filesystem
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Remove old image file if updating with a new one
        if self.pk:
            old_self = Post.objects.get(pk=self.pk)
            if self.image and old_self.image and old_self.image != self.image:
                if os.path.isfile(old_self.image.path):
                    os.remove(old_self.image.path)
        super().save(*args, **kwargs)
