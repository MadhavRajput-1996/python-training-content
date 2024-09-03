from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.core.validators import RegexValidator


class UserProfileInfo(models.Model):
    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Add any additional attributes you want
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    # Validators should be a list
    phone = models.CharField(
        validators=[phone_regex], max_length=17, blank=True)
    employee_id = models.CharField(max_length=10, unique=False)
    profile_pic = models.ImageField(
        upload_to='static/images/profile_pics', blank=True)
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.user.email})"

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.user.username})
