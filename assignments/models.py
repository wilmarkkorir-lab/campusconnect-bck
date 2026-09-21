from django.db import models
from django.conf import settings


class Assignment(models.Model):
    course = models.ForeignKey('academics.Course', on_delete=models.CASCADE, related_name='assignments')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=300)
    instructions = models.TextField()
    attachment = models.FileField(upload_to='assignments/', null=True, blank=True)
    deadline = models.DateTimeField()
    max_marks = models.PositiveSmallIntegerField(default=100)
    allow_submissions = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'assignments'
        ordering = ['deadline']

    def __str__(self):
        return f'{self.course.code} - {self.title}'


class Submission(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('late', 'Late Submission'),
        ('graded', 'Graded'),
        ('returned', 'Returned'),
    ]
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='submissions/', null=True, blank=True)
    text_response = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    graded_at = models.DateTimeField(null=True, blank=True)
    graded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='graded_submissions'
    )

    class Meta:
        db_table = 'submissions'
        unique_together = ('assignment', 'student')
        ordering = ['-submitted_at']

    def __str__(self):
        return f'{self.student.email} - {self.assignment.title}'
