from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notifications'),
    path('unread-count/', views.UnreadCountView.as_view(), name='unread_count'),
    path('mark-read/', views.MarkNotificationReadView.as_view(), name='mark_all_read'),
    path('<int:pk>/mark-read/', views.MarkNotificationReadView.as_view(), name='mark_read'),
    path('preferences/', views.NotificationPreferenceView.as_view(), name='notification_prefs'),
]
