from django.db import models
from django.conf import settings


class Club(models.Model):
    CLUB_TYPES = [
        ('technology', 'Technology'),
        ('sports', 'Sports'),
        ('academic', 'Academic'),
        ('entrepreneurship', 'Entrepreneurship'),
        ('cultural', 'Cultural'),
        ('volunteer', 'Volunteer'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    club_type = models.CharField(max_length=20, choices=CLUB_TYPES, default='other')
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='clubs/', null=True, blank=True)
    university = models.ForeignKey('universities.University', on_delete=models.CASCADE, related_name='clubs')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'clubs'

    def __str__(self):
        return self.name


class ClubMember(models.Model):
    ROLES = [('leader', 'Leader'), ('official', 'Official'), ('member', 'Member')]
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='club_memberships')
    role = models.CharField(max_length=10, choices=ROLES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'club_members'
        unique_together = ('club', 'user')

    def __str__(self):
        return f'{self.user.email} - {self.club.name}'


class ClubAnnouncement(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='announcements')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=300)
    content = models.TextField()
    attachment = models.FileField(upload_to='club_announcements/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'club_announcements'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.club.name} - {self.title}'
