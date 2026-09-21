from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.AdminDashboardStatsView.as_view(), name='admin_dashboard_stats'),
    path('daily/', views.AdminDailyStatsView.as_view(), name='admin_daily_stats'),
    path('activity/', views.UserActivityListView.as_view(), name='user_activity_list'),
    path('my-activity/', views.MyActivityView.as_view(), name='my_activity'),
    path('log/', views.LogActivityView.as_view(), name='log_activity'),
]
