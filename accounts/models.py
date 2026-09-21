from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import uuid


class Role(models.TextChoices):
    STUDENT = 'student', 'Student'
    LECTURER = 'lecturer', 'Lecturer'
    CLASS_REP = 'class_rep', 'Class Representative'
    CLUB_LEADER = 'club_leader', 'Club Leader'
    STUDENT_LEADER = 'student_leader', 'Student Leader'
    DEPT_ADMIN = 'dept_admin', 'Department Administrator'
    UNIVERSITY_ADMIN = 'university_admin', 'University Administrator'
    SUPER_ADMIN = 'super_admin', 'Super Administrator'


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', Role.SUPER_ADMIN)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_secret = models.CharField(max_length=64, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f'{self.email} ({self.role})'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_number = models.CharField(max_length=50, unique=True)
    university = models.ForeignKey('universities.University', on_delete=models.SET_NULL, null=True)
    campus = models.ForeignKey('universities.Campus', on_delete=models.SET_NULL, null=True, blank=True)
    faculty = models.ForeignKey('universities.Faculty', on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey('universities.Department', on_delete=models.SET_NULL, null=True, blank=True)
    program = models.ForeignKey('universities.Program', on_delete=models.SET_NULL, null=True, blank=True)
    year_of_study = models.PositiveSmallIntegerField(default=1)
    semester = models.PositiveSmallIntegerField(default=1)
    profile_photo = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(blank=True)
    skills = models.JSONField(default=list)
    interests = models.JSONField(default=list)
    profile_visibility = models.CharField(
        max_length=20,
        choices=[('public', 'Public'), ('students', 'Students Only'), ('private', 'Private')],
        default='students'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'students'

    def __str__(self):
        return f'{self.user.full_name} - {self.student_number}'


class LecturerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lecturer_profile')
    staff_number = models.CharField(max_length=50, unique=True)
    university = models.ForeignKey('universities.University', on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey('universities.Department', on_delete=models.SET_NULL, null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(blank=True)
    office_location = models.CharField(max_length=200, blank=True)
    office_hours = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'lecturers'

    def __str__(self):
        return f'{self.user.full_name} - {self.staff_number}'


class OTPVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps')
    code = models.CharField(max_length=6)
    purpose = models.CharField(max_length=30, choices=[
        ('email_verify', 'Email Verification'),
        ('password_reset', 'Password Reset'),
        ('two_factor', 'Two Factor Auth'),
    ])
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'otp_verifications'

    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at


class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    device = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    success = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'login_history'
        ordering = ['-created_at']


class BlockedUser(models.Model):
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_users')
    blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'blocked_users'
        unique_together = ('blocker', 'blocked')


class StudentLeaderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='leader_profile')
    university = models.ForeignKey('universities.University', on_delete=models.SET_NULL, null=True)
    position_title = models.CharField(max_length=200)
    office = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='leaders/', null=True, blank=True)
    term_start = models.DateField(null=True, blank=True)
    term_end = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'student_leader_profiles'

    def __str__(self):
        return f'{self.user.full_name} - {self.position_title}'


class ClassRepProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='classrep_profile')
    course = models.ForeignKey('academics.Course', on_delete=models.SET_NULL, null=True, blank=True)
    university = models.ForeignKey('universities.University', on_delete=models.SET_NULL, null=True)
    academic_year = models.CharField(max_length=20, blank=True)
    semester = models.PositiveSmallIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'class_rep_profiles'

    def __str__(self):
        return f'{self.user.full_name} - Class Rep'
