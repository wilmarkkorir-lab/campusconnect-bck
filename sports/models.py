from django.db import models
from django.conf import settings


class SportsTeam(models.Model):
    name = models.CharField(max_length=200)
    sport = models.CharField(max_length=100)
    university = models.ForeignKey('universities.University', on_delete=models.CASCADE, related_name='sports_teams')
    coach = models.CharField(max_length=200, blank=True)
    logo = models.ImageField(upload_to='sports/', null=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sports_teams'

    def __str__(self):
        return f'{self.name} ({self.sport})'


class TeamPlayer(models.Model):
    POSITIONS = [('player', 'Player'), ('captain', 'Captain'), ('vice_captain', 'Vice Captain')]
    team = models.ForeignKey(SportsTeam, on_delete=models.CASCADE, related_name='players')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sports_teams')
    position = models.CharField(max_length=15, choices=POSITIONS, default='player')
    jersey_number = models.PositiveSmallIntegerField(null=True, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'team_players'
        unique_together = ('team', 'user')


class Tournament(models.Model):
    name = models.CharField(max_length=200)
    sport = models.CharField(max_length=100)
    university = models.ForeignKey('universities.University', on_delete=models.CASCADE, related_name='tournaments')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tournaments'

    def __str__(self):
        return self.name


class Fixture(models.Model):
    RESULT_CHOICES = [('scheduled', 'Scheduled'), ('completed', 'Completed'), ('cancelled', 'Cancelled')]
    tournament = models.ForeignKey(Tournament, on_delete=models.SET_NULL, null=True, blank=True, related_name='fixtures')
    home_team = models.ForeignKey(SportsTeam, on_delete=models.CASCADE, related_name='home_fixtures')
    away_team = models.ForeignKey(SportsTeam, on_delete=models.CASCADE, related_name='away_fixtures')
    venue = models.CharField(max_length=200, blank=True)
    match_datetime = models.DateTimeField()
    home_score = models.PositiveSmallIntegerField(null=True, blank=True)
    away_score = models.PositiveSmallIntegerField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=RESULT_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fixtures'
        ordering = ['match_datetime']

    def __str__(self):
        return f'{self.home_team.name} vs {self.away_team.name}'
