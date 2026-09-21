from django.contrib import admin
from .models import ForumCategory, ForumPost, Comment, Reaction, PostBookmark


@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_question', 'is_pinned', 'views_count', 'created_at')
    list_filter = ('category', 'is_question', 'is_pinned', 'is_published')
    search_fields = ('title', 'content', 'author__email')
    actions = ['pin_posts', 'unpin_posts']

    def pin_posts(self, request, queryset):
        queryset.update(is_pinned=True)

    def unpin_posts(self, request, queryset):
        queryset.update(is_pinned=False)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'is_accepted_answer', 'created_at')
    list_filter = ('is_accepted_answer',)


admin.site.register(ForumCategory)
admin.site.register(Reaction)
admin.site.register(PostBookmark)
