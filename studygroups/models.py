from django.db import models
from django.conf import settings


class StudyGroup(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    course = models.ForeignKey('academics.Course', on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_study_groups')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='StudyGroupMember', related_name='study_groups')
    is_private = models.BooleanField(default=False)
    max_members = models.PositiveSmallIntegerField(default=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'study_groups'

    def __str__(self):
        return self.name


class StudyGroupMember(models.Model):
    ROLES = [('admin', 'Admin'), ('member', 'Member')]
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'study_group_members'
        unique_together = ('group', 'user')


class StudySession(models.Model):
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='sessions')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    scheduled_at = models.DateTimeField()
    duration_minutes = models.PositiveSmallIntegerField(default=60)
    location = models.CharField(max_length=200, blank=True)
    is_online = models.BooleanField(default=False)
    meeting_link = models.URLField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'study_sessions'
        ordering = ['scheduled_at']


class StudyGroupResource(models.Model):
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='resources')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=300)
    file = models.FileField(upload_to='study_groups/', null=True, blank=True)
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'study_group_resources'
