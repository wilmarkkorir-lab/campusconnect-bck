from django.db import models
from django.conf import settings


class Portfolio(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='portfolio')
    headline = models.CharField(max_length=300, blank=True)
    summary = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    share_token = models.CharField(max_length=64, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.share_token:
            import secrets
            self.share_token = secrets.token_urlsafe(48)
        super().save(*args, **kwargs)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'portfolios'

    def __str__(self):
        return f'{self.user.full_name} Portfolio'


class Project(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    technologies = models.JSONField(default=list)
    project_url = models.URLField(blank=True)
    repo_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='portfolio/projects/', null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_ongoing = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'portfolio_projects'
        ordering = ['-start_date']

    def __str__(self):
        return self.title


class Certificate(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='certificates')
    title = models.CharField(max_length=300)
    issuer = models.CharField(max_length=200)
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=200, blank=True)
    credential_url = models.URLField(blank=True)
    file = models.FileField(upload_to='portfolio/certificates/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'portfolio_certificates'
        ordering = ['-issue_date']

    def __str__(self):
        return f'{self.title} - {self.issuer}'


class Achievement(models.Model):
    ACHIEVEMENT_TYPES = [
        ('award', 'Award'),
        ('competition', 'Competition'),
        ('recognition', 'Recognition'),
        ('scholarship', 'Scholarship'),
        ('other', 'Other'),
    ]
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=300)
    achievement_type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPES, default='award')
    issuer = models.CharField(max_length=200, blank=True)
    date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'portfolio_achievements'
        ordering = ['-date']

    def __str__(self):
        return self.title


class WorkExperience(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='work_experiences')
    title = models.CharField(max_length=300)
    organization = models.CharField(max_length=200)
    employment_type = models.CharField(max_length=50, choices=[
        ('full_time', 'Full Time'), ('part_time', 'Part Time'),
        ('internship', 'Internship'), ('volunteer', 'Volunteer'),
        ('freelance', 'Freelance'),
    ], default='full_time')
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'work_experiences'
        ordering = ['-start_date']

    def __str__(self):
        return f'{self.title} at {self.organization}'


class Leadership(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='leadership_roles')
    role = models.CharField(max_length=300)
    organization = models.CharField(max_length=200)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'leadership_roles'
        ordering = ['-start_date']

    def __str__(self):
        return f'{self.role} at {self.organization}'
