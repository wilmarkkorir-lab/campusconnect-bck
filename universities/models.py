from django.db import models


class University(models.Model):
    name = models.CharField(max_length=200, unique=True)
    short_name = models.CharField(max_length=20, blank=True)
    logo = models.ImageField(upload_to='universities/', null=True, blank=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'universities'
        verbose_name_plural = 'Universities'

    def __str__(self):
        return self.name


class Campus(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='campuses')
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300, blank=True)
    is_main = models.BooleanField(default=False)

    class Meta:
        db_table = 'campuses'
        verbose_name_plural = 'Campuses'

    def __str__(self):
        return f'{self.university.short_name} - {self.name}'


class Faculty(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='faculties')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, blank=True)
    dean_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)

    class Meta:
        db_table = 'faculties'
        verbose_name_plural = 'Faculties'

    def __str__(self):
        return f'{self.university.short_name} - {self.name}'


class Department(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, blank=True)
    hod_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    office_location = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'departments'

    def __str__(self):
        return f'{self.faculty.university.short_name} - {self.name}'


class Program(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='programs')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, blank=True)
    duration_years = models.PositiveSmallIntegerField(default=4)
    degree_type = models.CharField(max_length=50, choices=[
        ('certificate', 'Certificate'),
        ('diploma', 'Diploma'),
        ('bachelors', "Bachelor's"),
        ('masters', "Master's"),
        ('phd', 'PhD'),
    ], default='bachelors')

    class Meta:
        db_table = 'programs'

    def __str__(self):
        return f'{self.name} ({self.code})'


class CampusLocation(models.Model):
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=[
        ('lecture_hall', 'Lecture Hall'),
        ('laboratory', 'Laboratory'),
        ('library', 'Library'),
        ('office', 'Office'),
        ('clinic', 'Clinic'),
        ('cafeteria', 'Cafeteria'),
        ('hostel', 'Hostel'),
        ('sports', 'Sports Facility'),
        ('parking', 'Parking'),
        ('student_center', 'Student Center'),
        ('other', 'Other'),
    ])
    building = models.CharField(max_length=100, blank=True)
    floor = models.CharField(max_length=20, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    description = models.TextField(blank=True)
    capacity = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'campus_locations'

    def __str__(self):
        return f'{self.campus.name} - {self.name}'
