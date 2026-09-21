from django.db import models
from django.conf import settings


class Exam(models.Model):
    EXAM_TYPES = [
        ('cat', 'CAT'),
        ('midterm', 'Midterm'),
        ('final', 'Final Exam'),
        ('supplementary', 'Supplementary'),
    ]
    course = models.ForeignKey('academics.Course', on_delete=models.CASCADE, related_name='exams')
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES)
    title = models.CharField(max_length=300)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=200, blank=True)
    location = models.ForeignKey(
        'universities.CampusLocation', on_delete=models.SET_NULL, null=True, blank=True
    )
    instructions = models.TextField(blank=True)
    max_marks = models.PositiveSmallIntegerField(default=100)
    semester = models.PositiveSmallIntegerField(default=1)
    academic_year = models.CharField(max_length=20, blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'exams'
        ordering = ['date', 'start_time']

    def __str__(self):
        return f'{self.course.code} - {self.exam_type} - {self.date}'


class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exam_results')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    grade = models.CharField(max_length=5, blank=True)
    remarks = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'exam_results'
        unique_together = ('exam', 'student')

    def __str__(self):
        return f'{self.student.email} - {self.exam}'
