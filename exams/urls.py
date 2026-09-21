from django.urls import path
from . import views

urlpatterns = [
    path('', views.ExamListView.as_view(), name='exam_list'),
    path('<int:pk>/', views.ExamDetailView.as_view(), name='exam_detail'),
    path('my-results/', views.MyExamResultsView.as_view(), name='my_results'),
    path('<int:exam_id>/results/', views.ExamResultsAdminView.as_view(), name='exam_results'),
]
