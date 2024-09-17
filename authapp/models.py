from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    full_name = models.CharField(max_length=255)
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    
    def __str__(self):
        return self.full_name
    
    def save(self, *args, **kwargs):
        if self.role == 'Admin':
            self.is_superuser = True
            self.is_staff = True
        else:
            self.is_superuser = False
            self.is_staff = False
        super().save(*args, **kwargs)
