from django.db import models
from django.conf import settings


class Job(models.Model):
    JOB_TYPES = [
        ('internship', 'Internship'),
        ('attachment', 'Attachment'),
        ('part_time', 'Part-Time'),
        ('graduate', 'Graduate Job'),
        ('campus', 'Campus Job'),
        ('freelance', 'Freelance'),
        ('volunteer', 'Volunteer'),
    ]
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    organization = models.CharField(max_length=200)
    title = models.CharField(max_length=300)
    job_type = models.CharField(max_length=15, choices=JOB_TYPES, default='internship')
    description = models.TextField()
    requirements = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    is_remote = models.BooleanField(default=False)
    deadline = models.DateField(null=True, blank=True)
    application_instructions = models.TextField(blank=True)
    application_url = models.URLField(blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'jobs'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} - {self.organization}'


class JobApplication(models.Model):
    STATUS_CHOICES = [('applied', 'Applied'), ('shortlisted', 'Shortlisted'), ('rejected', 'Rejected'), ('accepted', 'Accepted')]
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_applications')
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to='job_applications/', null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'job_applications'
        unique_together = ('job', 'applicant')

    def __str__(self):
        return f'{self.applicant.email} - {self.job.title}'
