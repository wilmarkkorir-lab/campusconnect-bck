from django.contrib import admin
from .models import University, Campus, Faculty, Department, Program, CampusLocation


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'is_active', 'created_at')
    search_fields = ('name', 'short_name')
    list_filter = ('is_active',)


@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ('name', 'university', 'is_main')
    list_filter = ('university', 'is_main')


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'university')
    search_fields = ('name', 'code')
    list_filter = ('university',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'faculty')
    search_fields = ('name', 'code')
    list_filter = ('faculty__university',)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'degree_type', 'duration_years')
    list_filter = ('degree_type',)
    search_fields = ('name', 'code')


@admin.register(CampusLocation)
class CampusLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'campus', 'category', 'building')
    list_filter = ('category', 'campus')
    search_fields = ('name', 'building')
