from django.urls import path
from . import views

urlpatterns = [
    path('', views.ScholarshipListView.as_view(), name='scholarship_list'),
    path('<int:pk>/', views.ScholarshipDetailView.as_view(), name='scholarship_detail'),
    path('<int:scholarship_id>/save/', views.SaveScholarshipView.as_view(), name='save_scholarship'),
    path('saved/', views.SavedScholarshipsView.as_view(), name='saved_scholarships'),
    path('applications/', views.ScholarshipApplicationView.as_view(), name='scholarship_applications'),
    path('applications/<int:pk>/', views.ScholarshipApplicationDetailView.as_view(), name='scholarship_application_detail'),
]
