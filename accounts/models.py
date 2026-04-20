from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    # Differenciated roles remain critical for system logic
    ROLE_CHOICES = [
        ('ATT', 'Attendee'),
        ('ORG', 'Organizer'),
        ('AMD', 'Administrator')
    ]
    role = models.CharField(max_length=3, choices=ROLE_CHOICES, default='ATT')
    
    # General Field for commercial Platform
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"