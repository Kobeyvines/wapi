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
    
class TicketTier(models.Model):
    TIER_CHOICES = [
        ('EB', 'Early Bird'), # Added comma
        ('REG', 'Regular'),   # Added comma
        ('VIP', 'VIP'),       # Added comma
    ]
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tiers')
    name = models.CharField(max_length=3, choices=TIER_CHOICES, default='REG')
    
    # Fixed: Changed 'max_digit' to 'max_digits' (it must be plural)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    capacity = models.PositiveIntegerField()
    quantity_sold = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.event.name} - {self.get_name_display()}"
    
class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket_tier = models.ForeignKey(TicketTier, on_delete=models.CASCADE, related_name='bookings')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    checkout_request_id = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    mpesa_receipt_number = models.CharField(max_length=50, blank=True, null=True)
    
def __str__(self):
        return f"{self.user.username} - {self.ticket_tier.event.name}"