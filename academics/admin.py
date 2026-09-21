from django.contrib import admin
from .models import Course, Enrollment, Material, MaterialCategory, MaterialBookmark, Timetable


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'department', 'lecturer', 'year_of_study', 'semester', 'is_active')
    list_filter = ('is_active', 'year_of_study', 'semester', 'department')
    search_fields = ('code', 'name')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('student__email', 'course__code')


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'material_type', 'uploaded_by', 'is_approved', 'download_count')
    list_filter = ('material_type', 'is_approved')
    search_fields = ('title', 'course__code')
    actions = ['approve_materials']

    def approve_materials(self, request, queryset):
        queryset.update(is_approved=True)
    approve_materials.short_description = 'Approve selected materials'


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('course', 'day', 'start_time', 'end_time', 'venue')
    list_filter = ('day', 'semester')


admin.site.register(MaterialCategory)
admin.site.register(MaterialBookmark)
