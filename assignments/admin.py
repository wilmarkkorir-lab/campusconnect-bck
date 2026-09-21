from django.contrib import admin
from .models import Assignment, Submission


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'deadline', 'allow_submissions', 'is_published')
    list_filter = ('is_published', 'allow_submissions', 'course')
    search_fields = ('title', 'course__code')


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'status', 'marks_obtained', 'submitted_at')
    list_filter = ('status',)
    search_fields = ('student__email', 'assignment__title')
