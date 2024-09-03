from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify

class UnderscoreCharField(models.CharField):
    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if value:
            value = value.replace(' ', '_').lower()
            setattr(model_instance, self.attname, value)
        return value

class SiteSettings(models.Model):
    key = UnderscoreCharField(max_length=250, unique=True)
    value = models.CharField(max_length=250)
    
    def __str__(self):
        return self.key



class EmailNotificationTemplate(models.Model):
    name = models.CharField(max_length=255, unique=False)
    slug = models.SlugField(max_length=255, unique=True)  # New field for slug
    subject = models.CharField(max_length=255)
    body = RichTextField()  # Use CKEditor for this field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
