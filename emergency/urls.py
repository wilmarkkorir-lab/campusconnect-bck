from django.urls import path
from . import views

urlpatterns = [
    path('contacts/', views.EmergencyContactListView.as_view(), name='emergency_contact_list'),
    path('contacts/<int:pk>/', views.EmergencyContactDetailView.as_view(), name='emergency_contact_detail'),
    path('announcements/', views.EmergencyAnnouncementListView.as_view(), name='emergency_announcement_list'),
    path('announcements/<int:pk>/', views.EmergencyAnnouncementDetailView.as_view(), name='emergency_announcement_detail'),
    path('incidents/', views.IncidentReportListView.as_view(), name='incident_report_list'),
    path('incidents/<int:pk>/', views.IncidentReportDetailView.as_view(), name='incident_report_detail'),
]
