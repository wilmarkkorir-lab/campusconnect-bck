from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, StudentProfile, LecturerProfile, OTPVerification, LoginHistory, BlockedUser


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'full_name', 'role', 'is_active', 'is_verified', 'date_joined')
    list_filter = ('role', 'is_active', 'is_verified', 'two_factor_enabled')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Role & Status', {'fields': ('role', 'is_active', 'is_verified', 'is_staff', 'is_superuser')}),
        ('Security', {'fields': ('two_factor_enabled', 'two_factor_secret', 'last_login_ip')}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_number', 'university', 'year_of_study', 'semester')
    search_fields = ('user__email', 'student_number')
    list_filter = ('year_of_study', 'semester', 'university')


@admin.register(LecturerProfile)
class LecturerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'staff_number', 'university', 'department')
    search_fields = ('user__email', 'staff_number')


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'success', 'created_at')
    list_filter = ('success',)
    readonly_fields = ('user', 'ip_address', 'user_agent', 'success', 'created_at')


admin.site.register(OTPVerification)
admin.site.register(BlockedUser)
