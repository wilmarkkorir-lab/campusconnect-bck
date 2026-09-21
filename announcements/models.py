from django.db import models
from django.conf import settings


class Announcement(models.Model):
    CATEGORY_CHOICES = [
        ('university', 'University'),
        ('department', 'Department'),
        ('course', 'Course'),
        ('lecturer', 'Lecturer'),
        ('registration', 'Registration'),
        ('fees', 'Fees'),
        ('examination', 'Examination'),
        ('emergency', 'Emergency'),
        ('safety', 'Safety'),
        ('general', 'General'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    title = models.CharField(max_length=300)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    university = models.ForeignKey(
        'universities.University', on_delete=models.CASCADE, null=True, blank=True
    )
    department = models.ForeignKey(
        'universities.Department', on_delete=models.SET_NULL, null=True, blank=True
    )
    course = models.ForeignKey(
        'academics.Course', on_delete=models.SET_NULL, null=True, blank=True
    )
    attachment = models.FileField(upload_to='announcements/', null=True, blank=True)
    is_published = models.BooleanField(default=True)
    publish_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'announcements'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
