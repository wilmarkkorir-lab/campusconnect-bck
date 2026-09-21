from django.db import models
from django.conf import settings


class FeeStructure(models.Model):
    """Published fee information from the university (read-only for students)."""
    university = models.ForeignKey('universities.University', on_delete=models.CASCADE, related_name='fee_structures')
    program = models.ForeignKey('universities.Program', on_delete=models.SET_NULL, null=True, blank=True)
    academic_year = models.CharField(max_length=20)
    semester = models.PositiveSmallIntegerField(null=True, blank=True)
    fee_type = models.CharField(max_length=50, choices=[
        ('tuition', 'Tuition Fee'),
        ('registration', 'Registration Fee'),
        ('accommodation', 'Accommodation Fee'),
        ('caution', 'Caution Money'),
        ('activity', 'Activity Fee'),
        ('other', 'Other'),
    ], default='tuition')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='KES')
    payment_deadline = models.DateField(null=True, blank=True)
    payment_instructions = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fee_structures'
        ordering = ['-academic_year', 'fee_type']

    def __str__(self):
        return f'{self.university.short_name} - {self.fee_type} ({self.academic_year})'
