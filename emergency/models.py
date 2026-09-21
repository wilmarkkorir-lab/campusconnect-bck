from django.db import models
from django.conf import settings


class EmergencyContact(models.Model):
    CONTACT_TYPES = [
        ('security', 'Campus Security'),
        ('clinic', 'Clinic / Medical'),
        ('admin', 'Administration'),
        ('fire', 'Fire Services'),
        ('police', 'Police'),
        ('ambulance', 'Ambulance'),
        ('counseling', 'Counseling / Support'),
        ('other', 'Other'),
    ]
    university = models.ForeignKey('universities.University', on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=200)
    contact_type = models.CharField(max_length=15, choices=CONTACT_TYPES, default='other')
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    available_hours = models.CharField(max_length=100, blank=True, default='24/7')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'emergency_contacts'

    def __str__(self):
        return f'{self.name} ({self.contact_type})'


class EmergencyAnnouncement(models.Model):
    university = models.ForeignKey('universities.University', on_delete=models.CASCADE, related_name='emergency_announcements')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=300)
    message = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'emergency_announcements'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class IncidentReport(models.Model):
    STATUS_CHOICES = [('submitted', 'Submitted'), ('under_review', 'Under Review'), ('resolved', 'Resolved')]
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    university = models.ForeignKey('universities.University', on_delete=models.CASCADE, related_name='incident_reports')
    title = models.CharField(max_length=300)
    description = models.TextField()
    location = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='submitted')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'incident_reports'
        ordering = ['-created_at']
