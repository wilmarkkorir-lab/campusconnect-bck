from django.urls import path
from . import views

urlpatterns = [
    path('', views.AssignmentListView.as_view(), name='assignment_list'),
    path('<int:pk>/', views.AssignmentDetailView.as_view(), name='assignment_detail'),
    path('<int:assignment_id>/submit/', views.SubmitAssignmentView.as_view(), name='submit_assignment'),
    path('<int:assignment_id>/submissions/', views.AssignmentSubmissionsView.as_view(), name='assignment_submissions'),
    path('submissions/<int:submission_id>/grade/', views.GradeSubmissionView.as_view(), name='grade_submission'),
    path('my-submissions/', views.MySubmissionsView.as_view(), name='my_submissions'),
]
