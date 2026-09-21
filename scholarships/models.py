from django.db import models
from django.conf import settings


class Scholarship(models.Model):
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=300)
    provider = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    eligibility = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    funding_amount = models.CharField(max_length=200, blank=True)
    is_fully_funded = models.BooleanField(default=False)
    deadline = models.DateField(null=True, blank=True)
    application_url = models.URLField(blank=True)
    application_instructions = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'scholarships'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.provider}'


class SavedScholarship(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_scholarships')
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE, related_name='saves')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'saved_scholarships'
        unique_together = ('user', 'scholarship')


class ScholarshipApplication(models.Model):
    STATUS_CHOICES = [('tracking', 'Tracking'), ('applied', 'Applied'), ('awarded', 'Awarded'), ('rejected', 'Rejected')]
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='scholarship_applications')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='tracking')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'scholarship_applications'
        unique_together = ('scholarship', 'user')
