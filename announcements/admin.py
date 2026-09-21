from django.contrib import admin
from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'priority', 'created_by', 'is_published', 'created_at')
    list_filter = ('category', 'priority', 'is_published')
    search_fields = ('title', 'content')
    actions = ['publish', 'unpublish']

    def publish(self, request, queryset):
        queryset.update(is_published=True)

    def unpublish(self, request, queryset):
        queryset.update(is_published=False)
