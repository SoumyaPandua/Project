from django.db import models
from django.conf import settings

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField()
    landmark = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    additional_info = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}'s Address"