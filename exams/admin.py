from django.contrib import admin
from .models import Exam, ExamResult


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'exam_type', 'date', 'start_time', 'venue', 'is_published')
    list_filter = ('exam_type', 'is_published', 'semester')
    search_fields = ('title', 'course__code')


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'marks_obtained', 'grade', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('student__email',)
