from django.contrib import admin
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation_type', 'name', 'created_by', 'created_at')
    list_filter = ('conversation_type',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'conversation', 'is_read', 'is_deleted', 'created_at')
    list_filter = ('is_read', 'is_deleted')
    search_fields = ('sender__email', 'content')
