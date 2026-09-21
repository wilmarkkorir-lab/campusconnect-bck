from django.db import models
from django.conf import settings


class Election(models.Model):
    STATUS_CHOICES = [('upcoming', 'Upcoming'), ('open', 'Open'), ('closed', 'Closed'), ('results_published', 'Results Published')]
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    university = models.ForeignKey('universities.University', on_delete=models.CASCADE, related_name='elections')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    nomination_start = models.DateTimeField()
    nomination_end = models.DateTimeField()
    voting_start = models.DateTimeField()
    voting_end = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'elections'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ElectionPosition(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='positions')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    max_votes_per_voter = models.PositiveSmallIntegerField(default=1)

    class Meta:
        db_table = 'election_positions'

    def __str__(self):
        return f'{self.election.title} - {self.title}'


class Candidate(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]
    position = models.ForeignKey(ElectionPosition, on_delete=models.CASCADE, related_name='candidates')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='candidacies')
    manifesto = models.TextField(blank=True)
    photo = models.ImageField(upload_to='candidates/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'candidates'
        unique_together = ('position', 'user')

    def __str__(self):
        return f'{self.user.full_name} - {self.position.title}'


class Vote(models.Model):
    position = models.ForeignKey(ElectionPosition, on_delete=models.CASCADE, related_name='votes')
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='votes_cast')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='votes_received')
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'votes'
        unique_together = ('position', 'voter')
