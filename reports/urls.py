from django.urls import path
from . import views

urlpatterns = [
    path('', views.SubmitReportView.as_view(), name='submit_report'),
    path('mine/', views.MyReportsView.as_view(), name='my_reports'),
    path('admin/', views.AdminReportListView.as_view(), name='admin_report_list'),
    path('admin/<int:pk>/', views.AdminReportDetailView.as_view(), name='admin_report_detail'),
    path('admin/<int:pk>/moderate/', views.ModerateReportView.as_view(), name='moderate_report'),
]
