from django.db import models
from django.conf import settings


class Conversation(models.Model):
    CONVERSATION_TYPES = [
        ('direct', 'Direct Message'),
        ('group', 'Group Chat'),
        ('class', 'Class Chat'),
        ('study_group', 'Study Group Chat'),
        ('club', 'Club Chat'),
    ]
    conversation_type = models.CharField(max_length=20, choices=CONVERSATION_TYPES, default='direct')
    name = models.CharField(max_length=200, blank=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'conversations'
        ordering = ['-updated_at']

    def __str__(self):
        return self.name or f'Conversation {self.id}'


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField(blank=True)
    file = models.FileField(upload_to='messages/', null=True, blank=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender.email}: {self.content[:50]}'


class MessageReadStatus(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='read_statuses')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'message_read_status'
        unique_together = ('message', 'user')
