from django.db import models
from django.conf import settings


class UserActivity(models.Model):
    ACTION_TYPES = [
        ('login', 'Login'),
        ('view_material', 'View Material'),
        ('download_material', 'Download Material'),
        ('submit_assignment', 'Submit Assignment'),
        ('post_forum', 'Post Forum'),
        ('join_study_group', 'Join Study Group'),
        ('view_job', 'View Job'),
        ('view_scholarship', 'View Scholarship'),
        ('register_event', 'Register Event'),
        ('send_message', 'Send Message'),
        ('view_course', 'View Course'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=30, choices=ACTION_TYPES)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    object_type = models.CharField(max_length=50, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_activities'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.email} - {self.action}'


class DailyStats(models.Model):
    date = models.DateField(unique=True)
    new_users = models.PositiveIntegerField(default=0)
    active_users = models.PositiveIntegerField(default=0)
    new_posts = models.PositiveIntegerField(default=0)
    new_materials = models.PositiveIntegerField(default=0)
    new_assignments = models.PositiveIntegerField(default=0)
    new_listings = models.PositiveIntegerField(default=0)
    new_jobs = models.PositiveIntegerField(default=0)
    new_events = models.PositiveIntegerField(default=0)
    messages_sent = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'daily_stats'
        ordering = ['-date']

    def __str__(self):
        return f'Stats for {self.date}'
