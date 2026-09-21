from django.db import models
from django.conf import settings


class Accommodation(models.Model):
    ACCOMMODATION_TYPES = [
        ('hostel', 'University Hostel'),
        ('private', 'Private Accommodation'),
        ('apartment', 'Apartment'),
        ('room', 'Single Room'),
        ('bed', 'Bed Space'),
    ]
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=300)
    accommodation_type = models.CharField(max_length=15, choices=ACCOMMODATION_TYPES, default='room')
    description = models.TextField(blank=True)
    location = models.CharField(max_length=300)
    university = models.ForeignKey('universities.University', on_delete=models.SET_NULL, null=True, blank=True)
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amenities = models.JSONField(default=list)
    contact_name = models.CharField(max_length=200, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    is_available = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'accommodation'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class AccommodationImage(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='accommodation/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'accommodation_images'
