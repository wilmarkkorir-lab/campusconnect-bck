from django.urls import path
from . import views

urlpatterns = [
    path('', views.JobListView.as_view(), name='job_list'),
    path('<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    path('<int:job_id>/apply/', views.JobApplyView.as_view(), name='job_apply'),
    path('<int:job_id>/applications/', views.JobApplicationsAdminView.as_view(), name='job_applications'),
    path('my-applications/', views.MyJobApplicationsView.as_view(), name='my_job_applications'),
]
