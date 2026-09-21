from django.db import models
from django.conf import settings


class MarketplaceListing(models.Model):
    CATEGORIES = [
        ('books', 'Books'),
        ('electronics', 'Electronics'),
        ('laptops', 'Laptops'),
        ('furniture', 'Furniture'),
        ('clothing', 'Clothing'),
        ('stationery', 'Stationery'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [('available', 'Available'), ('sold', 'Sold'), ('reserved', 'Reserved')]

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=300)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORIES, default='other')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'marketplace_listings'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} - {self.seller.email}'


class ListingImage(models.Model):
    listing = models.ForeignKey(MarketplaceListing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='marketplace/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'listing_images'


class SavedListing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_listings')
    listing = models.ForeignKey(MarketplaceListing, on_delete=models.CASCADE, related_name='saves')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'saved_listings'
        unique_together = ('user', 'listing')
