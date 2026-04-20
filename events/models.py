from django.db import models
from django.conf import settings
from django.utils.text import slugify
import uuid

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = "Categories"
        
    def __str__(self):
        return self.name
    
class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name='organized_events')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    venue = models.CharField(max_length=255)
    date = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    poster = models.ImageField(upload_to='events/posters/')
    
    # The Many-to-Many "Tag" Approach
    categories = models.ManyToManyField(Category, related_name='events')
    
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name