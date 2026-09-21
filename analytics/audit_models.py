from django.db import models
from django.conf import settings


class AuditLog(models.Model):
    ACTION_TYPES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('password_change', 'Password Change'),
        ('role_change', 'Role Change'),
        ('account_activate', 'Account Activate'),
        ('account_deactivate', 'Account Deactivate'),
        ('moderate', 'Moderation Action'),
        ('election_vote', 'Election Vote'),
        ('export', 'Data Export'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='audit_logs'
    )
    action = models.CharField(max_length=25, choices=ACTION_TYPES)
    model_name = models.CharField(max_length=100, blank=True)
    object_id = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'audit_logs'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} - {self.action} - {self.created_at}'
