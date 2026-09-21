from django.db import models
from django.conf import settings


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('message', 'Message'),
        ('announcement', 'Announcement'),
        ('assignment', 'Assignment'),
        ('exam', 'Exam'),
        ('event', 'Event'),
        ('study_group', 'Study Group'),
        ('job', 'Job'),
        ('scholarship', 'Scholarship'),
        ('marketplace', 'Marketplace'),
        ('forum', 'Forum'),
        ('club', 'Club'),
        ('election', 'Election'),
        ('emergency', 'Emergency'),
        ('system', 'System'),
    ]
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=300)
    message = models.TextField()
    link = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.recipient.email} - {self.title}'


class NotificationPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_prefs')
    messages = models.BooleanField(default=True)
    announcements = models.BooleanField(default=True)
    assignments = models.BooleanField(default=True)
    exams = models.BooleanField(default=True)
    events = models.BooleanField(default=True)
    study_groups = models.BooleanField(default=True)
    jobs = models.BooleanField(default=True)
    scholarships = models.BooleanField(default=True)
    marketplace = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)

    class Meta:
        db_table = 'notification_preferences'
