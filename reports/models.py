from django.db import models
from django.conf import settings


class Report(models.Model):
    REPORT_TYPES = [
        ('spam', 'Spam'),
        ('harassment', 'Harassment'),
        ('fake_account', 'Fake Account'),
        ('inappropriate_post', 'Inappropriate Post'),
        ('suspicious_listing', 'Suspicious Listing'),
        ('misleading_info', 'Misleading Information'),
        ('other', 'Other'),
    ]
    CONTENT_TYPES = [
        ('user', 'User'),
        ('forum_post', 'Forum Post'),
        ('comment', 'Comment'),
        ('marketplace_listing', 'Marketplace Listing'),
        ('accommodation', 'Accommodation'),
        ('message', 'Message'),
        ('club', 'Club'),
        ('job', 'Job'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]
    ACTION_CHOICES = [
        ('none', 'No Action'),
        ('warning', 'Warning Issued'),
        ('content_removed', 'Content Removed'),
        ('suspended', 'Account Suspended'),
        ('banned', 'Account Banned'),
    ]

    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='reports_made'
    )
    reported_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports_received'
    )
    report_type = models.CharField(max_length=25, choices=REPORT_TYPES)
    content_type = models.CharField(max_length=25, choices=CONTENT_TYPES, default='other')
    content_id = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports_reviewed'
    )
    action_taken = models.CharField(max_length=20, choices=ACTION_CHOICES, default='none')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reports'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.report_type} by {self.reported_by}'


class ModerationLog(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='moderation_logs')
    moderator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=Report.ACTION_CHOICES)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'moderation_logs'
        ordering = ['-created_at']

    def __str__(self):
        return f'Moderation on report {self.report_id} by {self.moderator}'
