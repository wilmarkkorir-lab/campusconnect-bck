from django.urls import path
from . import views

urlpatterns = [
    path('conversations/', views.ConversationListView.as_view(), name='conversations'),
    path('conversations/<int:pk>/', views.ConversationDetailView.as_view(), name='conversation_detail'),
    path('conversations/<int:conversation_id>/messages/', views.MessageListView.as_view(), name='messages'),
    path('messages/<int:message_id>/delete/', views.DeleteMessageView.as_view(), name='delete_message'),
    path('direct/', views.DirectMessageView.as_view(), name='direct_message'),
]
