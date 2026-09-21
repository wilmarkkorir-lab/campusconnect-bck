from django.db import models
from django.conf import settings
import uuid


class Event(models.Model):
    EVENT_TYPES = [
        ('hackathon', 'Hackathon'),
        ('conference', 'Conference'),
        ('workshop', 'Workshop'),
        ('career_fair', 'Career Fair'),
        ('club_event', 'Club Event'),
        ('sports', 'Sports Event'),
        ('training', 'Training'),
        ('meeting', 'Student Meeting'),
        ('other', 'Other'),
    ]
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='other')
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='organized_events')
    university = models.ForeignKey('universities.University', on_delete=models.CASCADE, null=True, blank=True)
    club = models.ForeignKey('clubs.Club', on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    location = models.CharField(max_length=300, blank=True)
    campus_location = models.ForeignKey('universities.CampusLocation', on_delete=models.SET_NULL, null=True, blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    banner = models.ImageField(upload_to='events/', null=True, blank=True)
    max_attendees = models.PositiveIntegerField(null=True, blank=True)
    requires_registration = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    meeting_link = models.URLField(blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'events'
        ordering = ['start_datetime']

    def __str__(self):
        return self.title


class EventRegistration(models.Model):
    STATUS_CHOICES = [('registered', 'Registered'), ('attended', 'Attended'), ('cancelled', 'Cancelled')]
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_registrations')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='registered')
    qr_code = models.UUIDField(default=uuid.uuid4, unique=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'event_registrations'
        unique_together = ('event', 'user')

    def __str__(self):
        return f'{self.user.email} - {self.event.title}'
