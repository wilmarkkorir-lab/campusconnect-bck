from django.db import models
from django.conf import settings


class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    department = models.ForeignKey('universities.Department', on_delete=models.SET_NULL, null=True)
    lecturer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='taught_courses', limit_choices_to={'role': 'lecturer'}
    )
    credits = models.PositiveSmallIntegerField(default=3)
    year_of_study = models.PositiveSmallIntegerField(default=1)
    semester = models.PositiveSmallIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'courses'

    def __str__(self):
        return f'{self.code} - {self.name}'


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments'
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'enrollments'
        unique_together = ('student', 'course')

    def __str__(self):
        return f'{self.student.email} - {self.course.code}'


class MaterialCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'material_categories'
        verbose_name_plural = 'Material Categories'

    def __str__(self):
        return self.name


class Material(models.Model):
    MATERIAL_TYPES = [
        ('notes', 'Notes'),
        ('slides', 'Slides'),
        ('pdf', 'PDF'),
        ('tutorial', 'Tutorial'),
        ('past_paper', 'Past Paper'),
        ('revision', 'Revision Material'),
        ('video', 'Video'),
        ('link', 'External Link'),
        ('other', 'Other'),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(MaterialCategory, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPES, default='notes')
    file = models.FileField(upload_to='materials/', null=True, blank=True)
    external_url = models.URLField(blank=True)
    is_approved = models.BooleanField(default=True)
    download_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'materials'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.course.code} - {self.title}'


class MaterialBookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'material_bookmarks'
        unique_together = ('user', 'material')


class Timetable(models.Model):
    DAYS = [
        ('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday'),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='timetable')
    day = models.CharField(max_length=10, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=200, blank=True)
    location = models.ForeignKey(
        'universities.CampusLocation', on_delete=models.SET_NULL, null=True, blank=True
    )
    semester = models.PositiveSmallIntegerField(default=1)
    academic_year = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = 'timetables'
        ordering = ['day', 'start_time']

    def __str__(self):
        return f'{self.course.code} - {self.day} {self.start_time}'


class AcademicCalendar(models.Model):
    EVENT_TYPES = [
        ('semester_start', 'Semester Start'),
        ('semester_end', 'Semester End'),
        ('holiday', 'Holiday'),
        ('registration', 'Registration Period'),
        ('exam_period', 'Exam Period'),
        ('cat_period', 'CAT Period'),
        ('assignment_deadline', 'Assignment Deadline'),
        ('graduation', 'Graduation'),
        ('other', 'Other'),
    ]
    university = models.ForeignKey(
        'universities.University', on_delete=models.CASCADE, related_name='calendar_events'
    )
    title = models.CharField(max_length=300)
    event_type = models.CharField(max_length=25, choices=EVENT_TYPES, default='other')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    academic_year = models.CharField(max_length=20, blank=True)
    semester = models.PositiveSmallIntegerField(null=True, blank=True)
    is_published = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'academic_calendar'
        ordering = ['start_date']

    def __str__(self):
        return f'{self.title} ({self.start_date})'


class PersonalReminder(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reminders'
    )
    title = models.CharField(max_length=300)
    note = models.TextField(blank=True)
    remind_at = models.DateTimeField()
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'personal_reminders'
        ordering = ['remind_at']

    def __str__(self):
        return f'{self.user.email} - {self.title}'
